''' Test for summarizer.py '''
from data_models.image import Image
from data_models.preprocessed_contents import PreprocessedContents
from summarization.summarizer_main import Summarizer


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
