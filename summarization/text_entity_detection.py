''' This module is used to define the TextEntityRetriever
for finding the named entities in the text.
The classes defined here are :
    * TextEntityRetriever
'''
import base64
import json
import os

import requests

from error import BadRequestError


class TextEntityRetriever:
    ''' Class to define the TextEntityRetriever
    methods:
        * _ready_data_for_post_request:
            gets the data ready for post request
            and formats it accordingly
        * get_entities_from_text:
            returns the entity present in the text as
            a list of strings
    '''
    API_ENDPOINT \
        = "https://language.googleapis.com/v1beta2/documents:analyzeEntities?key="  # noqa

    def __init__(self):
        self.api_key \
            = base64.b64decode(os.environ['GOOGLE_CLOUD_API_KEY'])\
                    .decode("utf-8")
        self.api_url \
            = self.API_ENDPOINT + self.api_key
        self.json_data_for_post_request = None

    def _ready_data_for_post_request(self, text):
        self.json_data_for_post_request = json.dumps({
            'document': {
                'type': 'PLAIN_TEXT',
                'content': text
            },
            "encodingType": 1
        })

    def get_entities_from_text(self, text):
        ''' Returns the entities as a list of strings
        Params:
            * text : a string of sentences
        Return type: list<str>
        '''
        self._ready_data_for_post_request(text)

        response = requests.post(
            self.api_url, data=self.json_data_for_post_request)

        if response.status_code != 200:
            raise BadRequestError(response.status_code)

        entities = json.loads(response.content)["entities"]
        entity_list = list()
        for entity_dict in entities:
            if entity_dict["type"] != 'OTHER':
                entity_list.append(entity_dict["name"])
        return entity_list
