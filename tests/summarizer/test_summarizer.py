''' Test for summarizer.py '''
from data_models.image import Image
from data_models.preprocessed_contents import PreprocessedContents
from summarization.summarizer import Summarizer


def test_image_with_caption_is_pruned():

    Image1 = Image(None, None, None, None)
    Image1.has_text_on_image = True

    Image2 = Image(None, None, None, None)
    Image2.has_text_on_image = False

    preprocessed_contents = PreprocessedContents(
        [], [], [Image1, Image2], [], []
    )

    summarizer = Summarizer(preprocessed_contents, 0, False)
    summarizer._create_stamps_and_filter_images_with_text()

    assert summarizer.contents.media == [Image2]


def test_capping_method_is_chosen_as_budgeted_max_cover():
    preprocessed_contents = PreprocessedContents(
        [], [], [], [], []
    )
    summarizer = Summarizer(preprocessed_contents, 0, False)

    page_limit = summarizer.MAX_PAGES_ALLOWED_FOR_BUDGETED_MAX_COVER

    summarizer.stamp_pages_list = ["stamp_page"] * (page_limit)
    summarizer._set_capping_method()
    assert summarizer.capping_method == summarizer.BUDGETED_MAX_COVER

    summarizer.stamp_pages_list = ["stamp_page"] * (page_limit - 1)
    summarizer._set_capping_method()
    assert summarizer.capping_method == summarizer.BUDGETED_MAX_COVER


def test_capping_method_is_chosen_as_interesting_sequence_picker():
    preprocessed_contents = PreprocessedContents(
        [], [], [], [], []
    )
    summarizer = Summarizer(preprocessed_contents, 0, False)

    page_limit = summarizer.MAX_PAGES_ALLOWED_FOR_BUDGETED_MAX_COVER

    summarizer.stamp_pages_list = [
        "stamp_page"] * (page_limit + 1)  # just above limit
    summarizer._set_capping_method()
    assert summarizer.capping_method == summarizer.INTERESTING_SEQUENCE_PICKER
