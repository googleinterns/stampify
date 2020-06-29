from summarization.text_media_matching.text_media_matching_preprocessor import \
    TextMediaMatchingPreprocessor  # noqa
from tests.summarizer.text_media_input_fetcher import fetch_text_media_input

# fetch test inputs
test_input_dict = fetch_text_media_input()
sentence_1 = test_input_dict["sentence_1"]
media_related_to_sentence_1 = test_input_dict["media_related_to_sentence_1"]

sentence_2 = test_input_dict["sentence_2"]
media_related_to_sentence_2 = test_input_dict["media_related_to_sentence_2"]


def test_text_media_preprocessor_return_format():
    ''' Tests if the return format of the preprocessor is correct'''
    preprocessor = TextMediaMatchingPreprocessor(
        [sentence_1],
        [media_related_to_sentence_1]
    )
    preprocessed_contents_dict = preprocessor.get_formatted_content()
    assert isinstance(preprocessed_contents_dict, dict)
    assert "sentences" in preprocessed_contents_dict
    assert "media" in preprocessed_contents_dict
    assert "content_unused_for_matching" in preprocessed_contents_dict


def test_text_media_preprocessor_eliminates_media():
    ''' Tests if preprocessor eliminates extra media'''
    preprocessor = TextMediaMatchingPreprocessor(
        [sentence_1],
        [media_related_to_sentence_2, media_related_to_sentence_1]
    )
    preprocessed_contents_dict = preprocessor.get_formatted_content()

    assert preprocessed_contents_dict["sentences"] == [sentence_1]
    assert preprocessed_contents_dict["media"] == [media_related_to_sentence_1]
    assert preprocessed_contents_dict["content_unused_for_matching"] == [
        media_related_to_sentence_2]


def test_text_media_preprocessor_eliminates_sentences():
    ''' Tests if pre-processor eliminates extra sentences'''
    preprocessor = TextMediaMatchingPreprocessor(
        [sentence_1, sentence_2],
        [media_related_to_sentence_2]
    )
    preprocessed_contents_dict = preprocessor.get_formatted_content()

    assert preprocessed_contents_dict["sentences"] == [sentence_2]
    assert preprocessed_contents_dict["media"] == [media_related_to_sentence_2]
    assert preprocessed_contents_dict["content_unused_for_matching"] == [
        sentence_1]


def test_text_media_preprocessor_returns_media_list_when_sentence_is_empty():
    ''' Media list is content unused for matching
    when sentence list is empty
    '''
    preprocessor = TextMediaMatchingPreprocessor(
        [],
        [media_related_to_sentence_1]
    )
    preprocessed_contents_dict = preprocessor.get_formatted_content()

    assert preprocessed_contents_dict["sentences"] == []
    assert preprocessed_contents_dict["media"] == []
    assert preprocessed_contents_dict["content_unused_for_matching"] == [
        media_related_to_sentence_1]


def test_text_media_preprocessor_returns_sentence_list_when_media_is_empty():
    ''' Sentence list is content unused
    when media list is empty
    '''
    preprocessor = TextMediaMatchingPreprocessor(
        [sentence_1],
        []
    )
    preprocessed_contents_dict = preprocessor.get_formatted_content()

    assert preprocessed_contents_dict["sentences"] == []
    assert preprocessed_contents_dict["media"] == []
    assert preprocessed_contents_dict["content_unused_for_matching"] == [
        sentence_1]


def test_text_media_preprocessor_returns_empty_unused_content_when_content_count_is_equal():  # noqa
    ''' Unused content is empty when sentence and media
    count are equal
    '''
    preprocessor = TextMediaMatchingPreprocessor(
        [sentence_1, sentence_2],
        [media_related_to_sentence_1, media_related_to_sentence_2]
    )
    preprocessed_contents_dict = preprocessor.get_formatted_content()

    assert preprocessed_contents_dict["sentences"] == [sentence_2, sentence_1]
    assert preprocessed_contents_dict["media"] == [
        media_related_to_sentence_1, media_related_to_sentence_2]
    assert preprocessed_contents_dict["content_unused_for_matching"] == []


def test_text_media_preprocessor_prunes_list():
    ''' Tests the pruning functionality'''
    preprocessor = TextMediaMatchingPreprocessor(
        [sentence_1, sentence_2],
        [media_related_to_sentence_1, media_related_to_sentence_2]
    )
    # the first 'count_content_to_eliminate' contents will be eliminated
    preprocessor.count_of_content_to_eliminate = 1
    filtered_list = preprocessor._get_pruned_list(
        [1, 0, 2],  # index 1 should be eliminated
        ['list_item1', 'list_item2', 'list_item3']
    )
    assert filtered_list == ['list_item1', 'list_item3']
    assert preprocessor.content_unused_for_matching == ['list_item2']
