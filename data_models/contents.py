"""This script creates object structure to store the extracted data
    and provides methods to set and retrieve the attributes"""

import enum


class Contents:
    """This class creates content_list which is list of extracted contents"""

    def __init__(self):
        self.content_list = list()
        self.content_counter = 0

    def add_content(self, _content):
        """This method appends extracted content to content_list"""
        _content.content_index = self.content_counter
        self.content_counter += 1
        self.content_list.append(_content)

    def get_content(self, index):
        """Return content at given index"""

        if not self.content_list:
            return None

        return self.content_list[index]

    def convert_to_dict(self):
        """This is custom method to convert the Contents
        object to dictionary"""

        # It will store list of dictionary representation of _Content object
        formatted_contents_list = list()

        for _content in self.content_list:
            formatted_contents_list.append(_content.__dict__)

        # It will store dictionary representation of Contents object
        formatted_contents = dict()

        for key, value in self.__dict__.items():
            if key == 'content_list':
                # Updating list of _Content object with
                # list of dictionary representation of _Content object
                formatted_contents[key] = formatted_contents_list
            else:
                formatted_contents[key] = value

        return formatted_contents


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
        return self.content_type.name


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

    def is_embedded_content(self):
        """Return true if content is embedded content"""

        return self.value in [
            self.EMBEDDED_INSTAGRAM_POST.value,
            self.EMBEDDED_PINTEREST_PIN.value,
            self.EMBEDDED_TWEET.value,
            self.EMBEDDED_YOUTUBE_VIDEO.value
        ]
