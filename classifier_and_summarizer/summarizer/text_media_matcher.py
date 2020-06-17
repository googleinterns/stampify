''' Text Media Matcher
This module contains utilities for matching
text and media .It uses the gale shapley algorithm
for finding the stable matching - and it is optimal
for the preference of the media.
This script contains the following classes:
    *ElementWithIndex : represent the text along with index
    *TextMediaMatcher : implements the main algorithm for matching
                        returns the stable matching
    *StableMatcher : implements the Gale-Shapley algorithm for matching
'''
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from classifier_and_summarizer.summarizer.incorrect_input import \
    IncorrectInputError
from classifier_and_summarizer.summarizer.stable_matcher import StableMatcher


class ElementWithIndex:
    ''' Pairs the element(summary sentence/image description)
    with the index of its occurence in the webpage
    '''

    def __init__(self, element_index, element_text):
        self.element_index = element_index
        self.element_text = element_text


class TextMediaMatcher:
    ''' Class containing utilties to find the Text-Media Matching
    Finds the stable matching by applying the Gale Shalpley algorithm
    It accepts a list of objects of type ElementWithIndex
    '''

    def __init__(self, summary_sentences,
                 media_descriptions, media_attributes):

        if len(summary_sentences) != len(media_attributes) or \
            len(summary_sentences) != len(media_descriptions) or \
                len(media_descriptions) != len(media_attributes):
            raise IncorrectInputError("Input sizes do not match")

        self.summary_sentences = summary_sentences
        self.media_descriptions = media_descriptions
        self.media_attributes = media_attributes
        self.set_size = len(media_descriptions)  # size of each set

        self.sentence_embedding_model = SentenceTransformer(
            'bert-base-nli-stsb-mean-tokens')

        # similarity matrix : will be used for sorting preferences
        # similarity score between ith summary_sentence and jth media
        # description
        self.similarity_matrix = [
            [-1 for i in range(self.set_size)] for j in range(self.set_size)]

        self.sentence_preference_for_media = [
            list(range(self.set_size)) for i in range(self.set_size)]
        self.media_preference_for_sentence = [
            list(range(self.set_size)) for i in range(self.set_size)]

    def get_text_media_matching(self):
        self._form_preference_matrix()
        stable_matcher = StableMatcher(
            self.media_preference_for_sentence,
            self.sentence_preference_for_media,
            self.set_size)
        return stable_matcher.get_matching()

    def __embed_text(self):
        '''finds the vector embeddings for necessary text'''
        self.summary_sentence_embeddings \
            = self.sentence_embedding_model.encode(
                [element.element_text for element in self.summary_sentences])

        self.media_description_embeddings \
            = self.sentence_embedding_model.encode(
                [element.element_text for element in self.media_descriptions])

        self.media_attribute_embeddings \
            = self.sentence_embedding_model.encode(
                [element.element_text for element in self.media_attributes])

    def __cosine_similarity_preprocessing(self):
        '''Calculates the required cosine similarity between matrices

        Finds the cosine similarity between summary sentences and
        media description and media attributes. This is done
        as preprocessing before calculating the similarity score
        '''
        self.similarity_matrix_for_media_descriptions = cosine_similarity(
            self.summary_sentence_embeddings,
            self.media_description_embeddings)

        self.similarity_matrix_for_media_attributes = cosine_similarity(
            self.summary_sentence_embeddings,
            self.media_attribute_embeddings)

    def __similarity_score(self, sentence_index, media_index):
        sentence_similarity_score = (
            1.0 + max(
                self.similarity_matrix_for_media_descriptions
                [sentence_index][media_index],
                self.similarity_matrix_for_media_attributes
                [sentence_index][media_index]))

        distance_score \
            = 1.0 + abs(
                self.media_attributes[media_index].element_index
                - self.summary_sentences[sentence_index].element_index
            )

        return sentence_similarity_score / distance_score

    def _form_preference_matrix(self):
        ''' Builds and initializes the preference matrix for media+sentences'''
        self.__embed_text()  # find the vector embeddings for both lists

        self.__cosine_similarity_preprocessing()

        for i in range(self.set_size):
            for j in range(self.set_size):
                self.similarity_matrix[i][j] = self.__similarity_score(
                    sentence_index=i, media_index=j)

        for i in range(self.set_size):
            self.media_preference_for_sentence[i].sort(
                key=lambda x: self.similarity_matrix[i][x], reverse=True)
            self.sentence_preference_for_media[i].sort(
                key=lambda x: self.similarity_matrix[x][i], reverse=True)
