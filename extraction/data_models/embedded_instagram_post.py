"""This class creates the object structure for Embedded Instagram content"""

from extraction.data_models.contents import ContentType, _Content


class EInstagramPost(_Content):
    """This class creates Embedded Instagram object"""

    def __init__(self, code, media_type=''):
        super(EInstagramPost, self).\
            __init__(ContentType.EMBEDDED_INSTAGRAM_POST)
        self.insta_shortcode = code
        self.media_type = media_type
