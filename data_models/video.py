"""This class creates the object structure for Video content"""

from data_models.contents import ContentType, _Content


class Video(_Content):
    """This class creates Video object"""

    def __init__(self, urls, height, width):
        super(Video, self).__init__(ContentType.VIDEO)
        self.video_urls = urls
        self.height = height
        self.width = width
