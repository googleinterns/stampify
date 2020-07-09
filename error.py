"""This script contains all errors"""


class StampifierError(Exception):
    """Base class for exceptions"""

    def __init__(self, message):
        super(StampifierError, self).__init__(message)
        self.message = message


class InvalidUrlError(StampifierError):
    """Raise exception when provided_url is invalid"""

    def __init__(self):
        super().__init__("Provided URL is Invalid!")


class NoneTypeMarkupError(StampifierError):
    """Raise when markup is NoneType"""

    def __init__(self):
        super().__init__('Expected markup string -> '
                         'Found NoneType!')


class WebsiteNotStampifiableError(StampifierError):
    """Raise when the provided website cannot be stampified"""

    def __init__(self, message, failure_source):
        super().__init__('{} Error received by: {}'
                         .format(message, failure_source))


class WebsiteConnectionError(StampifierError):
    """Raise when connection to website is not possible"""

    def __init__(self):
        super().__init__('Cannot connect to URL!')
