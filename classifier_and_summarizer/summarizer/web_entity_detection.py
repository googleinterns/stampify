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
import json
import os

import requests


class BadRequestError(Exception):
    '''Exception raised when the API call was not successfully'''

    def __init__(self, status_code):
        super(BadRequestError, self).__init__()
        self.message = "The API call was unsuccessful with status code: " + \
            str(status_code)


class ImageDescriptionRetriever:
    '''
    A class to retreive the entities present in an image
    Params:
      maxEntites : maximum number of entity results to return from the api
    '''

    def __init__(self, max_entities=3):
        self.api_url = base64.b64decode(
                os.environ['CLOUD_VISION_API_KEY']).decode("utf-8")
        self.max_entities = max_entities

    def get_description_for_images(self, images: list) -> list:
        '''
        given a list of images returns the best guess
        labels for the web entities or description of
        the images
        Params:
        images : list of image paths
        Return type:
        list<str> : list containing best guess descriptions of the image
        '''
        base64_encoded_images = self._find_base64_encoding_for_images(images)

        image_requests \
            = [self._format_single_request(encoded_image) for
                encoded_image in base64_encoded_images]

        json_data_for_post_request = json.dumps({
            "requests": image_requests
        })
        response = requests.post(self.api_url, data=json_data_for_post_request)

        if response.status_code != 200:
            raise BadRequestError(response.status_code)

        response = json.loads(response.content)
        image_descriptions = []
        for i in range(len(images)):
            image_descriptions.append(
                {
                    "label": self._get_best_guess_label(
                            response["responses"][i]
                            ),
                    "entities": self._get_top_entities(
                                response["responses"][i],
                                self.max_entities
                                )
                }
            )

        return image_descriptions

    def _find_base64_encoding_for_images(self, images: list) -> list:
        '''
        finds the base-64 encoding and converts it to a utf-8
        string
        Params :
            images : list of image paths
        Return type:
            list : of images encoded in the above format
        '''
        base64_encodings = []

        for image_path in images:
            with open(image_path, 'rb') as image_file:
                encoded_image = base64.encodebytes(image_file.read()).decode()
                base64_encodings.append(encoded_image)

        return base64_encodings

    def _format_single_request(self, data: str) -> dict:
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
                "content": data
            },
            "features": [
                {
                    "maxResults": self.max_entities,
                    "type": "WEB_DETECTION"
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
        return image_response["webDetection"]["bestGuessLabels"][0]["label"]

    def _get_top_entities(self, image_response, number_of_entities):
        ''' return the top entity description'''

        number_of_entities = min(number_of_entities, len(
            image_response["webDetection"]["webEntities"]))

        web_entity_collection \
            = image_response["webDetection"]["webEntities"]

        return [web_entity_collection[i]["description"]
                for i in range(number_of_entities)
                if "description" in web_entity_collection[i]]
