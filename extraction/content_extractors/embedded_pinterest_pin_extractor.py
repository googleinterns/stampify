"""This script checks whether DOM has pinterest pins tag or not and
creates and returns the EPinterestPin object"""

import bs4

from data_models.embedded_pinterest_pin import EPinterestPin
from extraction.content_extractors.interface_content_extractor import \
    IContentExtractor


class EPinterestPinExtractor(IContentExtractor):
    """This class inherits IContentExtractor for extracting
     embedded pinterest pins"""

    def validate_and_extract(self, node: bs4.element):
        if isinstance(node, bs4.element.Tag) \
                and node.name == 'a' \
                and node.has_attr('data-pin-do') \
                and node['data-pin-do'] == 'embedPin'\
                and node.has_attr('href'):
            return EPinterestPin(node['href'])

        return None
