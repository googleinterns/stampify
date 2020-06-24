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
from numpy import maximum as matrix_maximum
from sklearn.metrics.pairwise import cosine_similarity

from summarization.incorrect_input import IncorrectInputError
from summarization.text_media_matching.stable_matcher import StableMatcher


class TextMediaMatchingHelper:
    ''' Class containing utilties to help the Text-Media Matching
    Finds the stable matching by applying the Gale Shalpley algorithm
    It accepts a list of objects of type ElementWithIndex
    '''

    def __init__(self, text_contents, media_contents):
        '''
        Params:
            * text_contents : list of objects of type
            SentenceWithAttributes
            * media_contents : list of objects of type
            Image
        '''

        # both sets must be of same size for this to work
        if len(text_contents) != len(media_contents):
            raise IncorrectInputError(
                "Input sizes do not match for text media matching")

        self.text_contents = text_contents
        self.media_contents = media_contents
        self.set_size = len(media_contents)  # size of each set

        # description
        self.sentence_preference_for_media = [
            list(range(self.set_size)) for i in range(self.set_size)]
        self.media_preference_for_sentence = [
            list(range(self.set_size)) for i in range(self.set_size)]

    def get_text_media_matching(self):
        ''' returns the matching as a list of
        tuples (x,y) where x is the sentence
        object and y is the media(image)
        '''
        self._form_preference_matrix()

        stable_matcher = StableMatcher(
            self.media_preference_for_sentence,
            self.sentence_preference_for_media,
            self.set_size)

        matchings = stable_matcher.get_matching()

        self.text_media_matchings = []
        for sentence_index, media_index in matchings:
            self.text_media_matchings.append(
                (self.text_contents[sentence_index],
                 self.media_contents[media_index])
            )
        return self.text_media_matchings

    def _get_embedded_text(self):
        '''fetches the vector embeddings for any necessary text
        from the object itself.
        '''
        self.summary_sentence_embeddings \
            = [text.embedding for text in self.text_contents]

        self.media_description_embeddings = [
            media.img_description_embedding for media in self.media_contents]

        self.media_attribute_embeddings \
            = [media.img_attribute_embedding for media in self.media_contents]

    def _cosine_similarity_preprocessing(self):
        '''Calculates the required cosine similarity between matrices

        Finds the cosine similarity between summary sentences and
        media description and media attributes. This is done
        as preprocessing before calculating the similarity score
        '''
        # pick maximum similarity between
        # similarity between sentence and media description
        # similarity between sentence and media attributes
        self.similarity_matrix = matrix_maximum(
            cosine_similarity(
                self.summary_sentence_embeddings,
                self.media_description_embeddings
            ),
            cosine_similarity(
                self.summary_sentence_embeddings,
                self.media_attribute_embeddings
            )
        )

    def _similarity_score(self, sentence_index, media_index):
        ''' returns the similarity score'''

        # 1.0 is add in case of total dissimimlarity
        sentence_similarity_score = (
            1.0 + self.similarity_matrix[sentence_index][media_index])

        # 1.0 is added to prevent ZeroDivisionError if indices are same
        distance_score \
            = 1.0 + abs(
                self.media_contents[media_index].content_index
                - self.text_contents[sentence_index].index
            )

        return sentence_similarity_score / distance_score

    def _form_preference_matrix(self):
        ''' Builds and initializes the preference matrix for media+sentences'''
        self._get_embedded_text()  # get the vector embeddings for both lists

        self._cosine_similarity_preprocessing()

        for i in range(self.set_size):
            for j in range(self.set_size):
                self.similarity_matrix[i][j] = self._similarity_score(
                    sentence_index=i, media_index=j)

        for i in range(self.set_size):
            self.media_preference_for_sentence[i].sort(
                key=lambda x: self.similarity_matrix[i][x], reverse=True)
            self.sentence_preference_for_media[i].sort(
                key=lambda x: self.similarity_matrix[x][i], reverse=True)
