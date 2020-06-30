'''Module to define BadRquestError'''


class BadRequestError(Exception):
    '''Exception raised when the API call was not completed successfully'''

    def __init__(self, status_code):
        super(BadRequestError, self).__init__()
        self.message = "The API call was unsuccessful with status code: " + \
            str(status_code)
