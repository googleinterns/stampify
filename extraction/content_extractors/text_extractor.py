"""This script checks whether DOM has text tag or not and
creates and returns the Text object"""

import bs4

from data_models.text import Text
from extraction.content_extractors.interface_content_extractor import \
    IContentExtractor
from extraction.utils import string_utils as utils

TEXT_TAGS = ['p', 'span', 'code', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
MAX_CHILD = 3


class TextExtractor(IContentExtractor):
    """This class inherits IContentExtractor for extracting text"""

    def validate_and_extract(self, node: bs4.element):
        """Validates if a tag is text tag and
        returns the extracted data from the text tag in Text object"""

        if isinstance(node, bs4.element.Tag):
            text_data = node.get_text().strip()
            if (node.name in TEXT_TAGS) \
                    and not utils.empty_text(text_data):
                text_type = node.name
                is_bold = (node.find('strong') or node.find('b')) \
                    and len(node.contents) <= MAX_CHILD
                text_content = Text(text_data, text_type, is_bold)
                return text_content
        elif isinstance(node, bs4.element.NavigableString) \
                and not utils.empty_text(node):
            text_content = Text(node.strip())
            return text_content

        return None
