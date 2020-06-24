''' Interface for budgeted max cover'''

from summarization.stamp_page_picking.budgeted_max_cover_solver import \
    BudgetedMaxCoverSolver
from summarization.stamp_page_picking.max_cover_preprocessor import \
    BudgetedMaxCoverPreprocessor


class StampPagePicker:
    def __init__(self, stamp_pages, summary_sentences, max_pages_allowed):
        self.stamp_pages = stamp_pages
        self.summary_sentences = summary_sentences
        self.max_pages_allowed = max_pages_allowed
        self.threshold = 0.4  # arbitrary value - refine if necessary
        self.summary_sentence_embeddings = [
            sentence.embedding for sentence in self.summary_sentences]

    def get_capped_and_unused_stamp_pages(self):
        preprocessor = BudgetedMaxCoverPreprocessor(
            self.stamp_pages,
            self.summary_sentence_embeddings,
            self.threshold
        )
        preprocessed_covers = preprocessor.get_cover_objects_for_stamp_pages()

        budgeted_max_cover_solver = BudgetedMaxCoverSolver(
            preprocessed_covers, self.max_pages_allowed, len(
                self.summary_sentences))

        approximate_max_cover \
            = budgeted_max_cover_solver.find_approximate_maximum_cover()

        capped_stamp_page_indices = approximate_max_cover["best_cover"]

        return {
            "capped_stamp_pages": [
                self.stamp_pages[index] for index in capped_stamp_page_indices
            ],
            "unused_stamp_pages": [
                self.stamp_pages[index] for index in
                list(range(len(self.stamp_pages)))
                if index not in capped_stamp_page_indices]
        }
