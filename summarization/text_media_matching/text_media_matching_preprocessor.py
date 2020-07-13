''' This module pre-processes the Input
for the text media matcher
'''
from numpy import maximum as matrix_maximum
from sklearn.metrics.pairwise import cosine_similarity


class TextMediaMatchingPreprocessor:
    ''' Class containing the various
    utilities for pre-processing
    the text before passing it onto
    TextMediaMatchingHelper
    '''
    def __init__(self, sentence_list, media_list):
        '''
        sentence_list : list with objects of type SentenceWithAttributes
        media_list : list of objects of type media (Image/Gif/Video)
        '''
        self.sentence_list = sentence_list
        self.sentence_count = len(sentence_list)
        self.media_list = media_list
        self.media_count = len(media_list)

        self.unused_content_type = None

        # collect embeddings for sentences/media
        self.sentence_embeddings = [
            sentence.embedding for sentence in self.sentence_list
        ]
        self.media_description_embeddings = [
            media.img_description_embedding for media in self.media_list
        ]
        self.media_attribute_embeddings = [
            media.img_attribute_embedding for media in self.media_list
        ]

        # some media/sentences may be unused for matching
        # we package this separately so it can be used later
        self.content_unused_for_matching = list()

    def get_formatted_content(self):
        ''' Returns the pre-processed contents'''
        # make sure no content list is empty
        if self.media_count > 0 and self.sentence_count > 0:
            self._form_similarity_matrix()
            self._prune_larger_list()

        # if one of the content lists are empty
        # fully allot them to unused content
        elif self.sentence_count == 0:
            self.content_unused_for_matching = self.media_list
            self.unused_content_type = "media"
            self.media_list = list()

        else:
            self.content_unused_for_matching = self.sentence_list
            self.unused_content_type = "text"
            self.sentence_list = list()

        return {
            # two lists of equal size will be used for matching
            "sentences": self.sentence_list,
            "media": self.media_list,
            # this list can be used separately
            "content_unused_for_matching": self.content_unused_for_matching,
            "unused_content_type": self.unused_content_type
        }

    def _form_similarity_matrix(self):
        self.similarity_matrix = matrix_maximum(
            cosine_similarity(
                self.sentence_embeddings,
                self.media_description_embeddings),

            cosine_similarity(
                self.sentence_embeddings,
                self.media_attribute_embeddings
            )
        )

    def _initialize_and_sort_indices_for_lists(self):
        self.sentence_list_indices = list(range(self.sentence_count))
        self.media_description_list_indices = list(range(self.media_count))

        # sort them based on maximum similarity
        # to any content of the other type
        self.sentence_list_indices.sort(
            key=lambda x: max(self.similarity_matrix[x]))
        self.media_description_list_indices.sort(
            key=lambda x: max(self.similarity_matrix[:, x]))

    def _get_pruned_list(self, list_of_indices, list_of_content):
        # this will store the content we will use for matching
        filtered_list = list()

        indices_to_be_eliminated \
            = list_of_indices[: self.count_of_content_to_eliminate]

        # store the contents eliminated
        self.content_unused_for_matching \
            = [list_of_content[index] for index in indices_to_be_eliminated]

        # store contents to be used for matching
        filtered_list \
            = [list_of_content[index] for index in list_of_indices
               if index not in indices_to_be_eliminated]

        # return the filtered list
        return filtered_list

    def _prune_larger_list(self):
        '''prunes the larger of the two lists to make it
        equal in size to the smaller one.

        Strategy for pruning is as follows:
        Eliminate the sentences with the least maximum
        relatedness to any media. Similarly for media
        '''
        self._initialize_and_sort_indices_for_lists()

        # difference in sizes is how many contents
        # should be eliminated from larger list
        self.count_of_content_to_eliminate = int(abs(
            len(self.sentence_list) - len(self.media_list)))

        if self.media_count > self.sentence_count:
            # we need to eliminate some media
            self.unused_content_type = "media"
            self.media_list = self._get_pruned_list(
                self.media_description_list_indices, self.media_list)
        else:
            # we need to eliminate some sentences
            self.unused_content_type = "text"
            self.sentence_list = self._get_pruned_list(
                self.sentence_list_indices, self.sentence_list)
