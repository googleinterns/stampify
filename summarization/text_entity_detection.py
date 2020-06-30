import base64
import json
import os

import requests

from summarization.bad_request_error import BadRequestError


class TextEntityRetriever:

    API_ENDPOINT \
        = "https://language.googleapis.com/v1beta2/documents:analyzeEntities?key="  # noqa

    def __init__(self):
        self.api_key \
            = base64.b64decode(os.environ['GOOGLE_CLOUD_API_KEY'])\
                    .decode("utf-8")
        self.api_url \
            = self.API_ENDPOINT + self.api_key

    def _ready_data_for_post_request(self, text):
        self.json_data_for_post_request = json.dumps({
            'document': {
                'type': 'PLAIN_TEXT',
                'content': text
            },
            "encodingType": 1
        })

    def get_entities_from_text(self, text):
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
