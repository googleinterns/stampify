''' Class to define the IncorrectInputException'''


class IncorrectInputError(Exception):
    ''' Exception raised when the input format is wrong'''
    def __init__(self, message):
        super(IncorrectInputError, self).__init__()
        self.message = message
