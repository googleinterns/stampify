'''
Module for performing Stable Matching

it solves an instance of the stable marriage problem.
This is used as a utility for Text-Media Matching
'''


class StableMatcher:
    ''' Class to implement Stable matching

    This Class implements the stable matching
    using the gale shapley algorithm.
    '''
    def __init__(
            self,
            media_preference_for_sentence,
            sentence_preference_for_media,
            set_size):
        self.set_size = set_size
        self.media_preference_for_sentence = media_preference_for_sentence
        self.sentence_preference_for_media = sentence_preference_for_media

    def get_matching(self):
        return self.__gale_shapley_matching()

    def __media_rank_in_sentence_preference(self, sentence_index, media_index):
        return self.media_preference_for_sentence[sentence_index].index(
            media_index)

    def __sentence_has_better_preference(
            self, sentence_index, unmatched_index):
        return self.__media_rank_in_sentence_preference(
            sentence_index, unmatched_index) < \
            self.__media_rank_in_sentence_preference(
            sentence_index, self.media_matched_for_sentence[sentence_index])

    def __gale_shapley_matching(self):
        '''
        Finds the stable matching between the text and media
        Given two (n,n) matrices of preferences for the set of Sentences, Media
        finds the stable matching by running the gale-shapley
        matching algorithm
        Returns : a list of tuples where each tuple (x,y) means
        x = index of sentence
        y = index of media
        Thus, it returns the indices matched as a list of tuples
        '''
        # Make the matching optimal for the Media

        # -1 denotes it is currently unmatched
        self.sentence_matched_for_media = [-1] * self.set_size
        self.media_matched_for_sentence = [-1] * self.set_size

        self.count_of_unmatched_media = self.set_size

        while self.count_of_unmatched_media > 0:
            unmatched_media_index = -1  # no index found currently
            for i in range(self.set_size):
                if self.sentence_matched_for_media[i] == -1:
                    unmatched_media_index = i
                    break

            for i in self.sentence_preference_for_media[unmatched_media_index]:
                # the sentence is unmatched
                if self.media_matched_for_sentence[i] == -1:
                    # we can match the sentence directly
                    self.media_matched_for_sentence[i] = unmatched_media_index
                    self.sentence_matched_for_media[unmatched_media_index] = i
                    self.count_of_unmatched_media -= 1
                    break
                elif self.__sentence_has_better_preference(
                        i,
                        unmatched_media_index):
                    # i prefers the current media better
                    # unmatch media currently matched for sentence i
                    self.sentence_matched_for_media[
                        self.media_matched_for_sentence[i]] = -1
                    self.sentence_matched_for_media[unmatched_media_index] = i
                    self.media_matched_for_sentence[i] = unmatched_media_index
                    break

        matchings = [(self.sentence_matched_for_media[i], i)
                     for i in range(self.set_size)]
        return matchings
