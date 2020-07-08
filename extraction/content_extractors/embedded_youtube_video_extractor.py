"""This script checks whether DOM has embedded youtube
video tag or not and creates and returns the EYouTubeVideo object"""

from urllib.parse import urlparse

import bs4

from data_models.embedded_youtube_video import EYouTubeVideo
from extraction.content_extractors.interface_content_extractor import \
    IContentExtractor


class EYouTubeVideoExtractor(IContentExtractor):
    """This class inherits IContentExtractor for extracting
    embedded youtube video"""

    def validate_and_extract(self, node: bs4.element):
        if node.name == 'iframe' and node.has_attr('src')\
                and node['src'].startswith('https://www.youtube.com/embed/'):
            return EYouTubeVideo(self.__get_youtube_video_id(node['src']))

        return None

    @staticmethod
    def __get_youtube_video_id(url):
        return urlparse(url)[2].split('/')[2]
