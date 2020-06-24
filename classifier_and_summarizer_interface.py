''' This module contains the main interface definition
for the classifier and summarizer module
'''
from classifier_and_summarizer.classification.classifier_main import Classifier
from classifier_and_summarizer.summarization.extractor_output_preprocessor import \
    ExtractorOutputPreprocessor  # noqa
from classifier_and_summarizer.summarization.summarizer_main import Summarizer


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

    def preprocess_contents(self):
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
        self.preprocess_contents()

        # classify the page as stampifiable or not
        self.classify()

        if self.is_stampifiable:
            self.summarize()

        return {
            "is_stampifiable": self.is_stampifiable,
            "stamp_pages": self.stampified_pages
        }

    def classify(self):
        classifier = Classifier(
            normal_text_contents=self.normal_text_contents,
            title_text_contents=self.title_text_contents,
            media_contents=self.media_contents,
            embedded_contents=self.embedded_contents,
            max_pages=self.max_pages
        )
        self.is_stampifiable = classifier.is_page_stampifiable()

    def summarize(self):
        # block will be modified to add summarizer logic
        # once summarizer interface is designed
        summarizer = Summarizer(
            self.title_text_contents,
            self.normal_text_contents,
            self.media_contents,
            self.embedded_contents,
            self.max_pages
        )

        self.stampified_pages = summarizer.get_summarized_content()
