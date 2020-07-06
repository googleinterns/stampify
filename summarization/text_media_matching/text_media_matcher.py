''' Text Media  Matching interface '''
from summarization.text_media_matching.text_media_matching_helper import \
    TextMediaMatchingHelper
from summarization.text_media_matching.text_media_matching_preprocessor import \
    TextMediaMatchingPreprocessor  # noqa


class TextMediaMatcher:
    '''Class to integrate the TextMediaMatching utilities'''
    def __init__(self, text_contents, media_contents):
        self.text_contents = text_contents
        self.media_contents = media_contents

    def _get_matched_and_unmatched_contents(self):
        if len(self.text_contents) == 0 or len(self.media_contents) == 0:
            return {
                "matched_contents": [],
                "unused_contents": self.text_contents
                if len(self.text_contents) != 0 else self.media_contents
            }
        preprocessor = TextMediaMatchingPreprocessor(
            self.text_contents,
            self.media_contents
        )
        preprocessed_contents_dict = preprocessor.get_formatted_content()

        text_for_matching = preprocessed_contents_dict["sentences"]
        media_for_matching = preprocessed_contents_dict["media"]
        unused_contents \
            = preprocessed_contents_dict["content_unused_for_matching"]

        matcher = TextMediaMatchingHelper(
            text_for_matching, media_for_matching)
        matched_contents = matcher.get_text_media_matching()

        return {
            "matched_contents": matched_contents,
            "unused_contents": unused_contents
        }
