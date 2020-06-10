"""This class creates the object structure for Embedded YouTube content"""

from extraction.data_models.contents import ContentType, _Content


class EYouTubeVideo(_Content):
    """This class creates Embedded YouTube object"""

    def __init__(self, video_id):
        super(EYouTubeVideo, self).__init__(ContentType.EMBEDDED_YOUTUBE_VIDEO)
        self.yt_video_id = video_id
        self.height = 0
        self.width = 0
