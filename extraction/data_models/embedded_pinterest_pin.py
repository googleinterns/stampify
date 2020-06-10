"""This class creates the object structure for
Embedded Pinterest Pin content"""

from extraction.data_models.contents import ContentType, _Content


class EPinterestPin(_Content):
    """This class creates Embedded Pinterest Pin object"""

    def __init__(self, url):
        super(EPinterestPin, self).__init__(ContentType.EMBEDDED_PINTEREST_PIN)
        self.pin_url = url
