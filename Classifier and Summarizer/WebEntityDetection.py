import requests
import base64
import json


class ImageDescriptionRetriever:
    '''
    A class to retreive the entities present in an image
    Params:
      maxEntites : maximum number of entity results to return from the api
    '''

    def __init__(self, max_entities=3):
        self.api_url = base64.b64decode("aHR0cHM6Ly92aXNpb24uZ29vZ2xlYXBpcy5jb20vdjEvaW1hZ2VzOmFubm90YXRlP2tleT1BSXphU3lDV0ZEOWd4UDRSN0o4c1dTMGxkb1ZkcGJjaGNCNi1oeDA=").decode(
            "utf-8")  # to do: must hide this securely
        self.max_entities = max_entities

    def find_base64_encoding_for_images(self, images: list) -> list:
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
            with open(image_path, 'rb') as f:
                encoded_image = base64.encodebytes(f.read()).decode()
                base64_encodings.append(encoded_image)

        return base64_encodings

    def format_single_request(self, data: str) -> dict:
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

    def prepare_requests(self, encoded_images: list) -> list:
        '''
        prepares the requests for making calls
        to the api. Structures the given images
        in the format as expected by the API
        Params :
          encodedImages : list of base64 encoded images
        Return Type:
        list: of required format
        '''
        image_requests = []

        for image in encoded_images:
            image_requests.append(self.format_single_request(image))

        return image_requests

    def get_best_guess_label(self, json_response_for_image):
        ''' return the best guess label '''
        return json_response_for_image["webDetection"]["bestGuessLabels"][0]["label"]

    def get_top_entities(self, json_response_for_image, number_of_entities):
        ''' return the top entity description'''
        top_entites = []
        number_of_entities = min(number_of_entities, len(
            json_response_for_image["webDetection"]["webEntities"]))

        for i in range(number_of_entities):
            if "description" in json_response_for_image["webDetection"]["webEntities"][i]:
                top_entites .append(
                    json_response_for_image["webDetection"]["webEntities"][i]["description"])
        return top_entites

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
        base64_encoded_images = self.find_base64_encoding_for_images(images)

        image_requests = self.prepare_requests(base64_encoded_images)

        json_data_for_post_request = json.dumps({
            "requests": image_requests
        })
        response = requests.post(self.api_url, data=json_data_for_post_request)

        if response.status_code != 200:
            return "BadRequestError"

        response = json.loads(response.content)
        image_descriptions = []
        for i in range(len(images)):
            image_descriptions.append(
                {
                    "label": self.get_best_guess_label(response["responses"][i]),
                    # pass on only response for the image
                    "entities": self.get_top_entities(response["responses"][i], self.max_entities)
                    # add more fields / attributes as required
                }
            )

        return image_descriptions
