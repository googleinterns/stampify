''' A module to find the most interesting sequence
of stamp pages that can be displayed to the user
'''

from summarization.stamp_page_picking.max_cover_preprocessor import \
    BudgetedMaxCoverPreprocessor
from summarization.stamp_page_picking.scoring_utils import ScoringUtils


class InterestingSequencePicker:
    '''
    Finds the most interesting sequence for a
    given list of stamp pages
    Basic outline of algorithm:
    1: initialize seed stamp page
        go to step 2
    2: while stamp_pages can be picked
        > pick stamp page with best interestingness metric
        > remove it from the stamp pages so it wont be
            picked again
        > update last picked stamp page
        go to step 3
    3: if total count of stamp pages
        picked is less then max pages allowed go to step2
        else stop
    '''

    # threshold as used in the determining the cover
    # of the stamp page
    THRESHOLD = 0.5  # change as required

    def __init__(
            self,
            stamp_pages,
            summary_sentences,
            max_pages_allowed):
        self.stamp_pages = stamp_pages
        self.summary_sentence_embeddings = [
            sentence.embedding for sentence in
            summary_sentences
        ]
        self.max_pages_allowed = max_pages_allowed

        self.stamp_page_indices = list(range(len(self.stamp_pages)))

        self.cover_size = len(summary_sentences)

        # the final sequence that will be returned
        self.stamp_page_sequence = list()

        self._set_stamp_page_covers()

        self.scoring_util = ScoringUtils(
            stamp_pages,
            self.stamp_page_covers,
            self.cover_size
        )

        # the first stamp page is the title card
        # for the series of stamp pages
        # we will use that as the seed stamp pages
        self._set_seed_stamp_page()

    def get_interesting_sequence_and_unused_pages(self):
        for i in range(self.max_pages_allowed):
            # get the index of the next best stamp page
            stamp_page_index = self._get_next_best_stamp_page_index()

            # do not continue if no more stamp pages
            # are left to be picked
            if stamp_page_index == -1:
                break

            # append the stamp page at that index
            self.stamp_page_sequence.append(
                self.stamp_pages[stamp_page_index]
            )

            # update the cover for unpicked weights
            # calculation during next iteration
            self.scoring_util.pick_stamp_page_cover_at_index(stamp_page_index)

            # update last picked
            self.last_picked_stamp_page_index = stamp_page_index

        return {
            "capped_stamp_pages": self.stamp_page_sequence,
            "unused_stamp_pages": [
                # whatever indices are remaining are unpicked
                # and can be packaged as unused contents
                self.stamp_pages[index] for index in self.stamp_page_indices
            ]
        }

    def _get_next_best_stamp_page_index(self):
        ''' returns the index of the
        next best stamp page to pick given knowledge
        of the last picked stamp page
        '''

        if len(self.stamp_page_indices) == 0:
            return -1

        # sort based on interestingness metric
        self.stamp_page_indices.sort(
            key=self.scoring_util.interestingess_metric, reverse=True)

        # stamp page index at index 0 will have highest score
        next_best_index = self.stamp_page_indices[0]

        # set the last picked index
        self.scoring_util.update_last_picked_stamp_page(next_best_index)

        # pick the cover for that corresponding
        self.scoring_util.pick_stamp_page_cover_at_index(next_best_index)

        # pop the index from indices list so it's not
        # picked again
        self.stamp_page_indices.pop(0)

        return next_best_index

    def _set_seed_stamp_page(self):
        ''' This is the stamp page from which we'll
        construct our sequence
        '''
        self.last_picked_stamp_page_index = self.stamp_pages[0]
        self.scoring_util.pick_stamp_page_cover_at_index(0)
        self.stamp_page_indices.pop(0)

    def _set_stamp_page_covers(self):
        ''' find covers for stamp pages'''
        preprocessor = BudgetedMaxCoverPreprocessor(
            self.stamp_pages,
            self.summary_sentence_embeddings,
            self.THRESHOLD)
        self.stamp_page_covers \
            = preprocessor.get_cover_objects_for_stamp_pages()
