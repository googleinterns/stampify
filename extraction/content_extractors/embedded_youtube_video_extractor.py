"""This script checks whether DOM has embedded youtube
video tag or not and creates and returns the EYouTubeVideo object"""

import bs4

from data_models.embedded_youtube_video import EYouTubeVideo
from extraction.content_extractors.interface_content_extractor import \
    IContentExtractor
from extraction.utils import media_extraction_utils as utils


class EYouTubeVideoExtractor(IContentExtractor):
    """This class inherits IContentExtractor for extracting
    embedded youtube video"""

    def validate_and_extract(self, node: bs4.element):
        if node.name == 'iframe' and node.has_attr('src')\
                and utils.has_domain(node['src'],
                                     r'^https://www\.youtube\.com/embed'):
            return EYouTubeVideo(self.__get_youtube_video_id(node['src']))

        return None

    @staticmethod
    def __get_youtube_video_id(url):
        return url.split('/')[4].split('?')[0]
