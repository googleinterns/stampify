''' Module to perform text summarization'''

import string

from gensim.summarization.summarizer import summarize
from nltk.tokenize import sent_tokenize, word_tokenize
from summarizer import Summarizer
from summarizer.coreference_handler import CoreferenceHandler

from summarization.incorrect_input import IncorrectInputError
from summarization.text_entity_detection import TextEntityRetriever


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

    Summarizers used:
    bert-extractive-summarizer:
    https://pypi.org/project/bert-extractive-summarizer/

    gensim summarizer:
    https://radimrehurek.com/gensim/summarization/summariser.html
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
            handler = CoreferenceHandler(greedyness=.4)
            self.text_summarizer = Summarizer(
                model='distilbert-base-uncased',
                sentence_handler=handler)
        elif priority == "speed":
            self.text_summarizer = summarize
        else:
            raise IncorrectInputError(
                "priority must be either accuracy or speed")

    def _get_entites_from_text(self):
        entity_retriever = TextEntityRetriever()
        self.entity_list = entity_retriever.get_entities_from_text(self.text)

    def _cleaned_and_word_tokenized(self, text):
        # strip punctuations
        text = text.translate(str.maketrans('', '', string.punctuation))
        word_tokenized_text = word_tokenize(text)
        return [
            word.lower() for word in word_tokenized_text if word.isalnum()
        ]

    def _list_has_sublist(self, list_1, list_2):
        '''
        Returns true if list_1 has list_2
        as a sublist(subarray)
        '''
        list_1_len = len(list_1)
        list_2_len = len(list_2)
        for i in range(list_1_len - list_2_len + 1):
            if list_1[i:i + list_2_len] == list_2:
                return True

        return False

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

        self.text = text
        # get the entities in the text and store it
        # in a list
        self._get_entites_from_text()

        # preprocess the entities and keep
        processed_entity_list = [
            self._cleaned_and_word_tokenized(entity)
            for entity in self.entity_list
        ]

        sentence_tokenized_text = sent_tokenize(text)

        text_with_entities_list = list()

        # separate sentences into two:
        # those that contain entities
        # and those that don't
        for sentence in sentence_tokenized_text:
            sentence_has_entity = False
            cleaned_sentence = self._cleaned_and_word_tokenized(sentence)
            for entity in processed_entity_list:
                # if the cleaned entity is present
                # in the cleaned sentence
                if self._list_has_sublist(
                        cleaned_sentence, entity):
                    sentence_has_entity = True
                    break

            if sentence_has_entity:
                text_with_entities_list.append(sentence)

        # summarize the sentence that don't have entities
        tokenized_summarized_text \
            = sent_tokenize(
                self.text_summarizer(text, ratio)
            )

        # combines both enetity and non-entity sentences
        # in ORDER
        # order is necessary so the indexing
        # is preserved
        combined_summarized_text_list = list()

        # iterate over the un-summarized sentences
        # if the sentence has an entity or is in
        # the summarized sentences list add it to
        # the combined summarized list

        for sentence in sentence_tokenized_text:

            if sentence in text_with_entities_list \
                    or sentence in tokenized_summarized_text:
                combined_summarized_text_list.append(sentence)

        return ' '.join(combined_summarized_text_list)
