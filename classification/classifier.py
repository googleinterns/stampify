''' module to define the web-page stampifiable Classifier'''

from nltk.tokenize import word_tokenize

from error.stampifier_error import WebsiteNotStampifiableError


class Classifier:
    '''Class to determine if a webpage is stampable

    Detemines if a webpage is stampable based on the following
    max(media_count,text_count) + embedded_content_count >= min_pages
    '''

    def __init__(
            self,
            contents,
            max_pages,
            webpage_title):
        self.contents = contents
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
                max(
                    self.contents.get_normal_text_content_count(),
                    self.contents.get_title_text_content_count()
                ),
                self.contents.get_media_content_count()
            ) \
            + self.contents.get_embedded_content_count() \
            + self.contents.get_quoted_content_count() >= self.min_pages

        if not self.is_stampifiable:
            raise WebsiteNotStampifiableError(
                message="Website cannot be stampified!",
                failure_source="Classifier")

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
