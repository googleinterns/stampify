''' Module to pre-process the contents of a
stamp page before applying the budgeted max
cover solver
'''
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from summarization.stamp_page_picking.cover import Cover


class BudgetedMaxCoverPreprocessor:
    '''
    Class to define pre-processing
    utils for the budgeted max cover solver
    '''
    COST_FOR_TEXT_ONLY_STAMP = 2.0
    COST_FOR_EMBEDDED_STAMP = 1.5
    COST_FOR_VISUAL_STAMP = 1.0

    def __init__(self, stamp_pages, summary_sentence_embeddings, threshold):
        self.stamp_pages = stamp_pages
        self.summary_sentence_embeddings = summary_sentence_embeddings
        self.threshold = threshold

        self.stamp_pages_count = len(self.stamp_pages)
        self.summary_sentence_count = len(summary_sentence_embeddings)

    def get_cover_objects_for_stamp_pages(self):
        '''
        Constructs the Cover objects and returns
        them as a list
        '''
        cover_objects_list = list()

        # collect stamp descriptor embeddings
        self._collect_stamp_page_descriptor_embeddings()

        # get covers for all stamp pages
        covers = self._get_cover_over_sentences_for_stamp_pages()

        # get costs for all stamp pages
        costs = self._get_cost_for_stamp_pages()

        for index in range(self.stamp_pages_count):
            cover_objects_list.append(
                Cover(
                    covers[index],
                    costs[index],
                    index,
                    self.summary_sentence_count
                )
            )

        return cover_objects_list

    def _get_cost_for_stamp_pages(self):
        costs = list()
        for stamp_page in self.stamp_pages:
            # block will be amended to add supporting logic
            # for deciding costs based on stamp page
            # type and content present
            cost = None
            if stamp_page.is_embedded_content:
                cost = self.COST_FOR_EMBEDDED_STAMP
            elif stamp_page.media_index != -1:
                cost = self.COST_FOR_VISUAL_STAMP
            else:
                cost = self.COST_FOR_TEXT_ONLY_STAMP
            costs.append(cost)
        return costs

    def _collect_stamp_page_descriptor_embeddings(self):
        ''' Collects the stamp page descriptor embeddings
        from all stamp pages. the stamp descriptor embeddings
        depends on the type of the stamp page
        '''
        self.stamp_page_descriptor_embeddings = [
            stamp_page.stamp_descriptor_embedding for
            stamp_page in self.stamp_pages
        ]

    def _get_cover_over_sentences_for_stamp_pages(self):
        ''' Instantiates and returns a
        cover object for every stamp pages
        '''

        # define a function to set the cover for a
        # cell as 1 if its above threshold and 0
        # if its below
        def set_val(cell_value):
            return 1 if cell_value >= self.threshold else 0
        set_cover = np.vectorize(pyfunc=set_val)

        self.list_of_covers = set_cover(
            cosine_similarity(
                self.stamp_page_descriptor_embeddings,
                self.summary_sentence_embeddings
            )
        )
        return self.list_of_covers.tolist()
