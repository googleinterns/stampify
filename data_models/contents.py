"""This script creates object structure to store the extracted data
    and provides methods to set and retrieve the attributes"""

import enum


class Contents:
    """This class creates content_list which is list of extracted contents"""

    def __init__(self):
        self.content_list = list()

    def add_content(self, _content):
        """This method appends extracted content to content_list"""

        self.content_list.append(_content)
        self.__dict__['content_list'].remove(_content)
        self.__dict__['content_list'].append(_content.__dict__)


class _Content:
    """This class creates object representation for each extracted content"""

    def __init__(self, content_type):
        self.content_type = content_type
        # default value = -1 since field
        # has not been initialized and is
        # invalid currently
        self.content_index = -1

    def get_content_type(self):
        """Returns the content type of the content"""
        return self.content_type


class ContentType(enum.Enum):
    """This class creates enumerated constants for Content Type"""

    UNKNOWN = 1
    TEXT = 2    # data_models/test
    IMAGE = 3   # data_models/image
    VIDEO = 4   # data_models/video
    QUOTE = 5   # data_models/quote
    EMBEDDED_TWEET = 6  # data_models/embedded_tweet
    EMBEDDED_INSTAGRAM_POST = 7  # data_models/embedded_instagram_post
    EMBEDDED_PINTEREST_PIN = 8  # data_models/embedded_pinterest_pin
    EMBEDDED_YOUTUBE_VIDEO = 9  # data_models/embedded_youtube_video
