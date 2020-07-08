"""This script checks whether DOM has quote tag or not and
creates and returns the Quote object"""

import bs4

from data_models.quote import Quote
from extraction.content_extractors.interface_content_extractor import \
    IContentExtractor
from extraction.utils import string_utils as utils


class QuoteExtractor(IContentExtractor):
    """This class inherits IContentExtractor for extracting quote"""

    def validate_and_extract(self, node: bs4.element):
        if isinstance(node, bs4.element.Tag) \
                and node.name == 'q' \
                and not utils.empty_text(node.text):
            cite = None
            if node.has_attr('cite'):
                cite = node['cite']
            quote = Quote(node.text, cite)
            return quote

        return None
