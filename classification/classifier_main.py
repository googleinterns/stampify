''' module to define the web-page stampifiable Classifier'''

from nltk.tokenize import word_tokenize


class Classifier:
    '''Class to determine if a webpage is stampable

    Detemines if a webpage is stampable based on the following
    max(media_count,text_count) + embedded_content_count >= min_pages
    '''

    def __init__(
            self,
            normal_text_contents,
            title_text_contents,
            media_contents,
            embedded_contents,
            max_pages,
            webpage_title):
        self.normal_text_count = len(normal_text_contents)
        self.title_text_count = len(title_text_contents)
        self.media_count = len(media_contents)
        self.embedded_content_count = len(embedded_contents)
        # max pages is maximum number of stamp pages allowed
        # min pages is the minimum number of stamp pages
        # required
        self.min_pages = max_pages // 2

        self.webpage_title = webpage_title

    def classify(self):
        ''' classifies the web page as stampifiable or not
        and sets the is_stampifiable attribute accordingly
        '''
        # max is picked since some unused media/sentences
        # might still be used for stamp page contents
        self.is_stampifiable \
            = max(
                max(self.normal_text_count, self.title_text_count),
                self.media_count) \
            + self.embedded_content_count >= self.min_pages

    def is_page_stampifiable(self):
        ''' returns the is_stampifiable flag'''
        self.classify()
        return self.is_stampifiable

    def is_webpage_topic_plural(self):
        '''
        Returns True if the title topic
        is over multiple topics, False otherwise

        This checks for numeric values in the title
        string. This cannot detect words indicating
        quantities (such as "one")
        TODO : add more metrics for webpage topic
            plurality detection
        '''
        tokenized_words = word_tokenize(self.webpage_title)
        return any(token.isnumeric() for token in tokenized_words)
