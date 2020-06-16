"""This class creates the object structure for Quote content"""

from extraction.data_models.contents import ContentType, _Content


class Quote(_Content):
    """This class creates Quote object"""

    def __init__(self, q_content, cite):
        super(Quote, self).__init__(ContentType.QUOTE)
        self.q_content = q_content
        self.cite = cite
