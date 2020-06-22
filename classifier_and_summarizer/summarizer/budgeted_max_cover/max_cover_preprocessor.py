''' Module to pre-process the contents of a
stamp page before applying the budgeted max
cover solver
'''
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from classifier_and_summarizer.summarizer.budgeted_max_cover.cover import Cover


class BudgetedMaxCoverPreprocessor:

    def __init__(self, stamp_pages, summary_sentence_embeddings, threshold):
        self.stamp_pages = stamp_pages
        self.summary_sentence_embeddings = summary_sentence_embeddings
        self.threshold = threshold

        self.stamp_pages_count = len(self.stamp_pages)
        self.summary_sentence_count = len(summary_sentence_embeddings)

    def _get_cover_objects_for_stamp_pages(self):

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
            costs.append(1)  # unit cost as of now
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
        def f(x): return 1 if x >= self.threshold else 0
        set_cover = np.vectorize(pyfunc=f)

        self.list_of_covers = set_cover(
            cosine_similarity(
                self.stamp_page_descriptor_embeddings,
                self.summary_sentence_embeddings
            )
        )
        return self.list_of_covers.tolist()
