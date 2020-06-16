"""This class creates the object structure for Embedded YouTube content"""

from data_models.contents import ContentType, _Content


class EYouTubeVideo(_Content):
    """This class creates Embedded YouTube object"""

    def __init__(self, video_id, height=0, width=0):
        super(EYouTubeVideo, self).__init__(ContentType.EMBEDDED_YOUTUBE_VIDEO)
        self.yt_video_id = video_id
        self.height = height
        self.width = width
