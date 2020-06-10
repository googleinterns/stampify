"""This class creates the object structure for Video content"""

from extraction.data_models.contents import ContentType, _Content


class Video(_Content):
    """This class creates Video object"""

    def __init__(self):
        super(Video, self).__init__(ContentType.VIDEO)
        self.video_urls = list()
        self.height = 0
        self.width = 0
