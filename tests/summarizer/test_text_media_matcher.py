from summarization.text_media_matching.text_media_matcher import \
    TextMediaMatcher
from tests.summarizer.text_media_input_fetcher import fetch_text_media_input

# fetch test inputs
test_input_dict = fetch_text_media_input()
sentence_1 = test_input_dict["sentence_1"]
media_related_to_sentence_1 = test_input_dict["media_related_to_sentence_1"]

sentence_2 = test_input_dict["sentence_2"]
media_related_to_sentence_2 = test_input_dict["media_related_to_sentence_2"]


def test_text_media_matcher_return_format():
    ''' tests the return format of the text-media
    matcher
    '''
    matcher = TextMediaMatcher(
        [sentence_1, sentence_2],
        [media_related_to_sentence_1, media_related_to_sentence_2]
    )
    processed_contents_dict = matcher._get_matched_and_unmatched_contents()
    assert isinstance(processed_contents_dict, dict)
    assert 'matched_contents' in processed_contents_dict
    assert 'unused_contents' in processed_contents_dict


def test_text_media_matcher_matches_contents():
    ''' checks if the response returned is correct'''
    matcher = TextMediaMatcher(
        [sentence_2],
        [media_related_to_sentence_1, media_related_to_sentence_2]
    )
    processed_contents_dict = matcher._get_matched_and_unmatched_contents()

    assert processed_contents_dict['matched_contents'] == [
        (sentence_2, media_related_to_sentence_2)]
    assert processed_contents_dict['unused_contents'] == [
        media_related_to_sentence_1]


def test_text_media_matcher_returns_unused_media_when_sentences_is_empty():
    matcher = TextMediaMatcher(
        [],
        [media_related_to_sentence_1, media_related_to_sentence_2]
    )

    processed_contents_dict = matcher._get_matched_and_unmatched_contents()

    assert processed_contents_dict["matched_contents"] == []
    assert processed_contents_dict["unused_contents"] == [
        media_related_to_sentence_1, media_related_to_sentence_2
    ]


def test_text_media_matcher_returns_unused_sentences_when_media_is_empty():
    matcher = TextMediaMatcher(
        [sentence_1, sentence_2],
        []
    )

    processed_contents_dict = matcher._get_matched_and_unmatched_contents()

    assert processed_contents_dict["matched_contents"] == []
    assert processed_contents_dict["unused_contents"] == [
        sentence_1, sentence_2
    ]


def test_text_media_matcher_returns_empty_dict_when_both_are_empty():
    matcher = TextMediaMatcher(
        [],
        []
    )

    processed_contents_dict = matcher._get_matched_and_unmatched_contents()

    assert processed_contents_dict["matched_contents"] == []
    assert processed_contents_dict["unused_contents"] == []
