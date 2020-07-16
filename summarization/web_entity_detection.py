'''Web Entity Detection

This module uses google's cloud vision API's
web entity detection feature for finding the
entities present in an image

The script contains the following classes:
    *BadRequestError : a class to define the exception when the API call fails
    *ImageDescriptionRetreiver : implements the necessary utilities for calling
                                the api and formatting the response
'''

import base64
import concurrent.futures as cf
import json
import os

import requests
from nltk.tokenize import word_tokenize

from summarization.bad_request_error import BadRequestError
from utils.url_utils import convert_scheme_to_http


class ImageDescriptionRetriever:
    '''
    A class to retreive the entities present in an image
    Params:
      maxEntites : maximum number of entity results to return from the api
    '''

    API_ENDPOINT \
        = "https://vision.googleapis.com/v1/images:annotate?key="

    BATCH_SIZE = 5  # number of images per api request

    WORD_COUNT_TO_QUALIFY_AS_CAPTION = 15

    def __init__(self, max_entities=3):
        self.api_key \
            = base64.b64decode(os.environ['GOOGLE_CLOUD_API_KEY'])\
                    .decode("utf-8")
        self.api_url = self.API_ENDPOINT + self.api_key
        self.max_entities = max_entities

    def get_description_for_images(self, image_urls: list) -> list:
        '''
        given a list of images returns the best guess
        labels for the web entities or description of
        the images
        Params:
        images : list of image paths
        Return type:
        list<str> : list containing best guess descriptions of the image
        '''
        self.image_urls = image_urls

        # split into batches based on batch size
        self._split_into_batches()

        # make each request in a single thread
        # this is done since request natively only
        # allows one request per thread
        self._make_concurrent_requests()

        # we need to get the same order as
        # that of the given image_urls
        return self._get_ordered_and_combined_request_responses()

    def _split_into_batches(self):
        self.image_url_batches = list()
        num_image_urls = len(self.image_urls)
        i = 0
        while i < num_image_urls:
            self.image_url_batches.append(
                self.image_urls[i:min(i + self.BATCH_SIZE, num_image_urls)]
            )
            i += self.BATCH_SIZE

    def _make_concurrent_requests(self):
        self.all_responses_list = list()
        executor = cf.ThreadPoolExecutor(max_workers=4)
        future_list = [
            executor.submit(
                self._make_post_request,
                self.image_url_batches[i],
                i) for i in range(len(self.image_url_batches))]
        for future in cf.as_completed(future_list):
            self.all_responses_list.append(future.result())

    def _get_ordered_and_combined_request_responses(self):
        # sort based on request number
        self.all_responses_list.sort()
        image_descriptions = list()
        for _, img_desc in self.all_responses_list:
            image_descriptions.extend(img_desc)

        return image_descriptions

    def _make_post_request(self, image_urls, request_number):
        # request number will be used to order
        # all the requests finally
        image_requests \
            = [self._format_single_request(url) for
               url in image_urls]

        json_data_for_post_request = json.dumps({
            "requests": image_requests
        })
        response = requests.post(self.api_url, data=json_data_for_post_request)

        if response.status_code != 200:
            print(response.content)
            raise BadRequestError(response.status_code)

        response = json.loads(response.content)
        image_descriptions = []
        for i in range(len(image_urls)):
            image_descriptions.append(
                {
                    "label": self._get_best_guess_label(
                        response["responses"][i]),

                    "entities": self._get_top_entities(
                        response["responses"][i],
                        self.max_entities),

                    "has_caption": self._get_text_annotation_is_below_limit(
                        response["responses"][i]
                    ),

                    "image_colors": self._get_top_colors_from_image(
                        response["responses"][i])})
        return request_number, image_descriptions

    def _format_single_request(self, url: str) -> dict:
        '''
        formats the request as a dict
        with the required data and returns it
        Params :
          data : a base64-encoded image as a utf-8 string
        Return type:
          dict : formatted as shown below
        '''
        return {
            "image": {
                "source": {
                    "imageUri": convert_scheme_to_http(url)
                }
            },
            "features": [
                {
                    "maxResults": self.max_entities,
                    "type": "WEB_DETECTION"
                },
                {
                    "type": "TEXT_DETECTION"
                },
                {
                    # only take top 3 colors
                    "maxResults": 3,
                    "type": "IMAGE_PROPERTIES"
                }
            ],
            "imageContext": {
                "webDetectionParams": {
                    "includeGeoResults": "true"
                }
            }
        }

    def _get_best_guess_label(self, image_response):
        ''' return the best guess label '''
        if "error" in image_response or "label" \
                not in image_response["webDetection"]["bestGuessLabels"][0]:
            return ""
        return image_response["webDetection"]["bestGuessLabels"][0]["label"]

    def _get_top_entities(self, image_response, number_of_entities):
        ''' return the top entity description'''

        if "error" in image_response:
            return [""]

        number_of_entities = min(number_of_entities, len(
            image_response["webDetection"]["webEntities"]))

        web_entity_collection \
            = image_response["webDetection"]["webEntities"]

        return [web_entity_collection[i]["description"]
                for i in range(number_of_entities)
                if "description" in web_entity_collection[i]]

    def _get_rgb_tuple_from_color_dict(self, color_dict):
        return (
            color_dict["color"]["red"],
            color_dict["color"]["green"],
            color_dict["color"]["blue"]
        )

    def _get_top_colors_from_image(self, image_response):
        if "imagePropertiesAnnotation" not in image_response:
            return [(-1, -1, -1)]  # return no image color found
        image_colors = list()

        for color_dict in image_response[
                "imagePropertiesAnnotation"]["dominantColors"]["colors"]:
            image_colors.append(
                self._get_rgb_tuple_from_color_dict(color_dict)
            )

        return image_colors

    def _get_word_count_from_text(self, text):
        # remove newline chars from text
        text = ' '.join(text.split('\n'))
        return len(word_tokenize(text))

    def _get_text_annotation_is_below_limit(self, image_response):
        if "textAnnotation" not in image_response:
            return False

        return self._get_word_count_from_text(
            image_response["textAnnotation"][0]["description"]
        ) >= self.WORD_COUNT_TO_QUALIFY_AS_CAPTION
