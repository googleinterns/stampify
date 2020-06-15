import pytest

from classifier_and_summarizer.summarizer.stable_matcher import StableMatcher
from classifier_and_summarizer.summarizer.text_media_matcher import (
    ElementWithIndex, IncorrectInputError, TextMediaMatcher)


def test_incorrect_input():
    ''' Tests error condition when input format is wrong'''
    with pytest.raises(IncorrectInputError) as error:
        summary_sentences = ["A", "B", "C"]
        media_descriptions = ["A", "B"]
        media_attributes = ["A", "B"]
        TextMediaMatcher(
            summary_sentences,
            media_descriptions,
            media_attributes)
        assert error.message \
            == "Sizes of Summary Sentences and Media description do not match"


def test_formation_of_preference_matrix():
    ''' Tests if the preference matrix is formed correctly'''
    summary_sentences = [
        ElementWithIndex(
            0, "Google was founded by Larry Page and Sergey Brin"),
        ElementWithIndex(
            0, "The Page Rank algorithm was named after Larry Page"),
        ElementWithIndex(
            0, "Google is a company that \
                specializes in internet related services")
    ]

    media_description = [
        ElementWithIndex(0, "Page Rank Algorithm Larry Page"),
        ElementWithIndex(0, "Google company logo"),
        ElementWithIndex(0, "Larry Page and Sergey Brin Google")
    ]

    media_attributes = [
        ElementWithIndex(0, "Page rank photo"),
        ElementWithIndex(0, "Google"),
        ElementWithIndex(0, "Google co-founders")
    ]

    text_media_matcher = TextMediaMatcher(
        summary_sentences, media_description, media_attributes)

    text_media_matcher._form_preference_matrix()

    assert text_media_matcher.sentence_preference_for_media == [
        [1, 0, 2],
        [2, 0, 1],
        [0, 1, 2]
    ]

    assert text_media_matcher.media_preference_for_sentence == [
        [2, 1, 0],
        [0, 2, 1],
        [1, 2, 0]
    ]


def test_stable_matching():
    ''' Tests if the stable matching algorithm produces
    the right output
    '''
    preference_matrix_1 = [[0, 2, 1, 3], [
        2, 3, 0, 1], [3, 1, 2, 0], [2, 1, 0, 3]]
    preference_matrix_2 = [[1, 0, 2, 3], [
        3, 0, 1, 2], [0, 2, 1, 3], [1, 2, 0, 3]]
    stable_matcher = StableMatcher(preference_matrix_1, preference_matrix_2, 4)
    expected_matching = [(0, 0), (3, 1), (2, 2), (1, 3)]
    actual_matching = stable_matcher.get_matching()
    assert expected_matching == actual_matching


def test_matching_with_same_indices():
    ''' Tests matching with elements of same indices

    Since indices are same the matching should be based on only
    similarity of content
    '''
    summary_sentence_0 = ElementWithIndex(
        0, "The Boys is a Tv show that packs grit and humor")
    summary_sentence_1 = ElementWithIndex(
        0, "Breaking Bad is a series that revolves around drama and crime")

    media_descripion_0 = ElementWithIndex(0, "Breaking Bad Bryan Cranston")
    media_descripion_1 = ElementWithIndex(0, "The Boys TV Show")

    media_attribute_0 = ElementWithIndex(0, "Breaking Bad")
    media_attribute_1 = ElementWithIndex(0, "The Boys")

    expected_matching = [(0, 1), (1, 0)]

    text_media_matcher = TextMediaMatcher(
        [summary_sentence_0, summary_sentence_1],
        [media_descripion_0, media_descripion_1],
        [media_attribute_0, media_attribute_1]
    )
    matching_found = sorted(text_media_matcher.get_text_media_matching())

    assert matching_found == expected_matching


def test_matching_with_different_indices():
    ''' Tests matching with different indices'''
    summary_sentence_0 = ElementWithIndex(
        0, "The Boys is a Tv show that packs grit and humor")
    summary_sentence_1 = ElementWithIndex(
        2, "Breaking Bad is a series that revolves around drama and crime")

    media_descripion_0 = ElementWithIndex(1, "Breaking Bad Bryan Cranston")
    media_descripion_1 = ElementWithIndex(3, "The Boys TV Show")

    media_attribute_0 = ElementWithIndex(1, "Breaking Bad")
    media_attribute_1 = ElementWithIndex(3, "The Boys")

    expected_matching = [(0, 1), (1, 0)]

    text_media_matcher = TextMediaMatcher(
        [summary_sentence_0, summary_sentence_1],
        [media_descripion_0, media_descripion_1],
        [media_attribute_0, media_attribute_1]
    )
    matching_found = sorted(text_media_matcher.get_text_media_matching())

    assert matching_found == expected_matching


def test_matching_with_different_indices_and_bad_attributes():
    ''' Tests matching when the attributes are bad

    This ensures that the matcher takes only maximum of
    similarity between attributes and entity descriptions
    '''
    summary_sentence_0 = ElementWithIndex(
        0, "The Boys is a Tv show that packs grit and humor")
    summary_sentence_1 = ElementWithIndex(
        0, "Breaking Bad is a series that revolves around drama and crime")

    media_descripion_0 = ElementWithIndex(0, "Breaking Bad Bryan Cranston")
    media_descripion_1 = ElementWithIndex(0, "The Boys TV Show")

    media_attribute_0 = ElementWithIndex(0, "hx1257")
    media_attribute_1 = ElementWithIndex(0, "cBuyI98")

    expected_matching = [(0, 1), (1, 0)]

    text_media_matcher = TextMediaMatcher(
        [summary_sentence_0, summary_sentence_1],
        [media_descripion_0, media_descripion_1],
        [media_attribute_0, media_attribute_1]
    )
    matching_found = sorted(text_media_matcher.get_text_media_matching())

    assert matching_found == expected_matching


def test_matching_with_spread_out_content():
    ''' Tests matching when the text related to the
    media is spread out and not closeby
    '''
    summary_sentence_0 = ElementWithIndex(
        6, "The Boys is a Tv show that packs grit and humor")
    summary_sentence_1 = ElementWithIndex(
        7, "Breaking Bad is a series that revolves around drama and crime")

    media_descripion_0 = ElementWithIndex(0, "Breaking Bad Bryan Cranston")
    media_descripion_1 = ElementWithIndex(13, "The Boys TV Show")

    media_attribute_0 = ElementWithIndex(0, "Breaking Bad")
    media_attribute_1 = ElementWithIndex(13, "The Boys")

    expected_matching = [(0, 1), (1, 0)]

    text_media_matcher = TextMediaMatcher(
        [summary_sentence_0, summary_sentence_1],
        [media_descripion_0, media_descripion_1],
        [media_attribute_0, media_attribute_1]
    )
    matching_found = sorted(text_media_matcher.get_text_media_matching())

    assert matching_found == expected_matching


def test_matching_with_similar_content():
    ''' Tests matching when the content of the
    media and texts are almost identical but still
    distinguishable from a human perspective
    '''
    summary_sentence_0 = ElementWithIndex(
        0, "Bryan Cranston is the lead actor of the TV series Breaking Bad")
    summary_sentence_1 = ElementWithIndex(
        0, "Breaking Bad is a series that revolves around drama and crime")

    media_descripion_0 = ElementWithIndex(0, "Breaking Bad TV Series")
    media_descripion_1 = ElementWithIndex(0, "Bryan Cranston")

    media_attribute_0 = ElementWithIndex(0, "Breaking Bad")
    media_attribute_1 = ElementWithIndex(0, "Actor")

    expected_matching = [(0, 1), (1, 0)]

    text_media_matcher = TextMediaMatcher(
        [summary_sentence_0, summary_sentence_1],
        [media_descripion_0, media_descripion_1],
        [media_attribute_0, media_attribute_1]
    )
    matching_found = sorted(text_media_matcher.get_text_media_matching())

    assert matching_found == expected_matching
