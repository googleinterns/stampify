"""This script checks whether DOM has video tag or not and
creates and returns the Video object"""

import re

import bs4

from data_models.video import Video
from extraction.content_extractors.interface_content_extractor import \
    IContentExtractor
from extraction.utils import media_extraction_utils as e_utils
from utils import url_utils

VIDEO_EXTENSIONS_PATTERN = re.compile(r'^.*\.(mp4|ogg|mov|webm)')


class VideoExtractor(IContentExtractor):
    """This class inherits IContentExtractor for extracting video"""

    def validate_and_extract(self, node: bs4.element):
        video_urls = list()
        if isinstance(node, bs4.element.Tag):
            if node.name == 'video':
                if node.has_attr('src'):
                    self.__append_video_url(video_urls, node['src'])
                elif node.contents:
                    for child in node.contents:
                        if child and child.name == 'source'\
                                and child.has_attr('src'):
                            self.__append_video_url(video_urls, child['src'])
            elif node.name == 'embed' \
                    and node.has_attr('src') \
                    and VIDEO_EXTENSIONS_PATTERN.match(node['src']):
                self.__append_video_url(video_urls, node['src'])

            if video_urls:
                height, width = e_utils.get_media_size(node)
                return Video(video_urls, height, width)

        return None

    def __append_video_url(self, video_urls, url):
        """If valid video url, append for extraction"""

        video_url = url_utils.valid_url(url)
        if video_url:
            video_urls.append(video_url)
