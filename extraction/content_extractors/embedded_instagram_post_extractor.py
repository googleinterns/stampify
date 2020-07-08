"""This script checks whether DOM has embedded instagram
post tag or not and creates and returns the EInstagramPost object"""

from urllib.parse import urlparse

import bs4

from data_models.embedded_instagram_post import EInstagramPost
from extraction.content_extractors.interface_content_extractor import \
    IContentExtractor


class EInstagramPostExtractor(IContentExtractor):
    """This class inherits IContentExtractor for extracting
    embedded instagram post"""

    def validate_and_extract(self, node: bs4.element):
        """Validates if a tag is instagram post tag and
        returns the extracted data from the tag in EInstagramPost object"""

        if isinstance(node, bs4.element.Tag):
            if node.has_attr('class') \
                and ('instagram-media' in node['class']
                     or 'instagram-media-rendered' in node['class']):
                return EInstagramPost(self.
                                      __get_instagram_shortcode
                                      (node.find('a')['href']))

            if node.name == 'iframe' \
                and node.has_attr('src') \
                    and node['src'].startswith('https://instagram.com/'):
                return EInstagramPost(self.
                                      __get_instagram_shortcode
                                      (node['src']))

        return None

    @staticmethod
    def __get_instagram_shortcode(url):
        return urlparse(url)[2].split('/')[2]
