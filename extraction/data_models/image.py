"""This class creates the object structure for Image content"""

from extraction.data_models.contents import ContentType, _Content


class Image(_Content):
    """This class creates Image object"""

    def __init__(self):
        super(Image, self).__init__(ContentType.IMAGE)
        self.img_url = ''
        self.img_caption = ''
        self.img_title = ''
        self.img_type = ''
        self.img_height = 0
        self.img_width = 0
        self.is_gif = False
