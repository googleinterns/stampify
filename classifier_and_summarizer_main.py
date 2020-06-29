''' This module contains the main interface definition
for the classifier and summarizer module
'''
from classification.classifier_main import Classifier
from summarization.extractor_output_preprocessor import \
    ExtractorOutputPreprocessor
from summarization.summarizer_main import Summarizer


class ClassifierAndSummarizer:
    def __init__(self, contents, max_pages):
        '''
        Params:
          * contents : an object of type contents
            it contains the contents_list
          * max_pages : the maximum pages required
        '''
        self.contents = contents
        self.max_pages = max_pages
        self.is_stampifiable = False
        # object of type StampPages
        self.stampified_pages = None

    def _preprocess_contents(self):
        '''
        This method will use ExtractorOutputPreprocessor
        to split the contents into different types
        '''
        output_preprocessor = ExtractorOutputPreprocessor(self.contents)
        self.preprocessed_contents_dict \
            = output_preprocessor.get_preprocessed_content_lists()
        self.title_text_contents \
            = self.preprocessed_contents_dict["titles"]
        self.normal_text_contents \
            = self.preprocessed_contents_dict["sentences"]
        self.media_contents = self.preprocessed_contents_dict["media"]
        self.embedded_contents \
            = self.preprocessed_contents_dict["embedded_content"]

    def get_stampified_content(self):
        ''' returns the list of stamp pages'''
        # pre-process the contents first
        self._preprocess_contents()

        # classify the page as stampifiable or not
        self._classify()

        # early return when the pages are not
        # stampifiable
        if not self.is_stampifiable:
            return {
                "is_stampifiable": self.is_stampifiable,
                "stamp_pages": None
            }

        # summarize
        self._summarize()
        # order the stamp pages
        self._order_stamp_pages()

        return {
            "is_stampifiable": self.is_stampifiable,
            "stamp_pages": self.stampified_pages
        }

    def _classify(self):
        classifier = Classifier(
            normal_text_contents=self.normal_text_contents,
            title_text_contents=self.title_text_contents,
            media_contents=self.media_contents,
            embedded_contents=self.embedded_contents,
            max_pages=self.max_pages
        )
        self.is_stampifiable = classifier.is_page_stampifiable()

    def _summarize(self):
        summarizer = Summarizer(
            self.title_text_contents,
            self.normal_text_contents,
            self.media_contents,
            self.embedded_contents,
            self.max_pages
        )

        self.stampified_pages = summarizer.get_summarized_content()

    def _get_min_index_for_stamp_page(self, stamp_page):
        indices = list()
        if stamp_page.sentence_index != -1:
            indices.append(stamp_page.sentence_index)

        if stamp_page.media_index != -1:
            indices.append(stamp_page.media_index)

        return min(indices)

    def _order_stamp_pages(self):
        # separate this as function so
        # logic can be amended to include
        # more information if necessary
        self.stampified_pages.stamp_pages.sort(
            key=self._get_min_index_for_stamp_page)
