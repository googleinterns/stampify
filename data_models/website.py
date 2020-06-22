"""This script creates a class to store
information about to a website"""

import validators


class Website:
    """This class stores the information about a website"""

    __LOGO_API = 'https://www.google.com/s2/favicons?domain='

    def __init__(self, url):
        self.url = url
        self.is_valid = validators.url(self.url) is True
        self.domain = self.url.split('/')[2] if self.is_valid else None
        self.logo_url = self.__LOGO_API + self.domain if self.domain else None
        self.contents = None

    def set_contents(self, contents):
        self.contents = contents
        self.__dict__.update({'contents': self.contents.__dict__})
