''' Module to perform text summarization'''

from gensim.summarization.summarizer import summarize
from summarizer import Summarizer

from classifier_and_summarizer.summarizer.incorrect_input import \
    IncorrectInputError


class TextSummarizer:
    """
    A class to perform summarization on english text

    Attributes:
        text_summarizer : will hold the summarizer chosen
        on the basis of priority

    Methods:
        - summarize_text (text , ratio):
            Given the text and ratio
            returns the summarized text
    """

    def __init__(self, priority):
        '''
        Initializes the text rank or bert summarizers
        based on priority

        priority should be either accuracy or speed
        based on which we can choose either a
        low speed high accuracy summarizer - bert
        high speed lower accuracy summarizer - textRank
        '''
        self.text_summarizer = None
        if priority == "accuracy":
            self.text_summarizer = Summarizer(model='distilbert-base-uncased')
        elif priority == "speed":
            self.text_summarizer = summarize
        else:
            raise IncorrectInputError(
                    "priority must be either accuracy or speed")

    def summarize_text(self, text: str, ratio=0.4):
        '''
            Finds the summarization for a given text

            Parameters:
                - text : the text to be summarized
                - ratio : value in range [0,1] - what % of the text to retain
        '''
        if ratio < 0 or ratio > 1:
            raise IncorrectInputError(
                "Ratio should be in the range of [0,1] ")

        return self.text_summarizer(text, ratio)
