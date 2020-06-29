import pytest

from summarization.incorrect_input import IncorrectInputError
from summarization.text_media_matching.text_media_matching_helper import \
    TextMediaMatchingHelper
from tests.summarizer.text_media_input_fetcher import fetch_text_media_input

# fetch test inputs
test_input_dict = fetch_text_media_input()
sentence_1 = test_input_dict["sentence_1"]
media_related_to_sentence_1 = test_input_dict["media_related_to_sentence_1"]

sentence_2 = test_input_dict["sentence_2"]
media_related_to_sentence_2 = test_input_dict["media_related_to_sentence_2"]


def test_text_media_matching_helper_throws_error_for_different_input_sizes():
    with pytest.raises(IncorrectInputError) as error:
        TextMediaMatchingHelper(
            [sentence_1],
            [media_related_to_sentence_2, media_related_to_sentence_1]
        )
        assert error.message \
            == "Input sizes do not match for text media matching"


def test_text_media_matching_helper_forms_preference_matrix():
    ''' Tests creation of preference matrix'''
    helper = TextMediaMatchingHelper(
        [sentence_1, sentence_2],
        [media_related_to_sentence_2, media_related_to_sentence_1]
    )
    helper._form_preference_matrix()
    assert helper.media_preference_for_sentence == [
        [1, 0],
        [0, 1]
    ]

    assert helper.sentence_preference_for_media == [
        [1, 0],
        [0, 1]
    ]


def test_text_media_matching_helper_returns_correct_matching():
    ''' checks if the matching is correct'''
    helper = TextMediaMatchingHelper(
        [sentence_1, sentence_2],
        [media_related_to_sentence_2, media_related_to_sentence_1]
    )
    expected_matching = [
        (sentence_1, media_related_to_sentence_1),
        (sentence_2, media_related_to_sentence_2)
    ]

    actual_matching = helper.get_text_media_matching()

    assert actual_matching == expected_matching
