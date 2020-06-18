"""This script checks whether DOM has text tag or not and
creates and returns the Text object"""

import bs4

from data_models.text import Text
from extraction.content_extractors.interface_content_extractor import \
    IContentExtractor
from extraction.utils import string_utils as utils


class TextExtractor(IContentExtractor):
    def validate_and_extract(self, node: bs4.element):
        """Validates if a tag is text tag and
        returns the extracted data from the text tag in Text object"""

        if isinstance(node, bs4.element.Tag):
            text_data = node.get_text().strip()
            if (node.name in utils.TEXT_TAGS) \
                    and not utils.empty_text(text_data) \
                    and utils.is_important_text(node):
                text_type = node.name
                text_content = Text(text_data, text_type)
                return text_content
        elif isinstance(node, bs4.element.NavigableString) \
                and not utils.empty_text(node) \
                and len(node) > utils.TEXT_MIN_SCORE:
            text_data = node.strip()
            text_content = Text(text_data)
            return text_content

        return None
