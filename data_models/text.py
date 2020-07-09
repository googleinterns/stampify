"""This class creates the object structure for Text content"""

from data_models.contents import ContentType, _Content


class Text(_Content):
    """This class creates Text object"""
    TITLE_CONTENT_TYPES = [
        "h1", "h2", "h3", "h4", "h5", "h6"
    ]

    def __init__(self, text_str, text_type='', is_bold=False):
        super(Text, self).__init__(ContentType.TEXT)
        self.type = text_type
        self.text_string = text_str
        self.font_style = ''
        self.is_bold = is_bold

    def is_important_text(self):
        """Checks the importance of text"""

        return self.type in self.TITLE_CONTENT_TYPES \
            or self.is_bold
