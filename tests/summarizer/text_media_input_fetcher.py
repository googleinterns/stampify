import json

from data_models.image import Image
from summarization.extractor_output_preprocessor import SentenceWithAttributes

with open('tests/summarizer/text_media_input.json', 'r') as json_input_file:
    test_input_dict = json.load(json_input_file)

# sentence about Sundar Pichai
sentence_1 = SentenceWithAttributes(
    "Sundar Pichai is the current CEO of Alphabet",
    0,
    None,
    test_input_dict["sentence_1_embedding"]
)

# Sentence about Larry Page
sentence_2 = SentenceWithAttributes(
    "Larry Page was one of the original founders",
    0,
    None,
    test_input_dict["sentence_2_embedding"]
)

# Image of Larry Page
media_related_to_sentence_2 = Image(
    "larry_page_img_url",
    None,
    None,
    None
)
media_related_to_sentence_2.img_attribute_embedding \
    = media_related_to_sentence_2.img_description_embedding \
    = test_input_dict["media_related_to_sentence_2_embedding"]
media_related_to_sentence_2.content_index = 0

# Image of Sundar Pichai
media_related_to_sentence_1 = Image(
    "sundar_pichai_img_url",
    None,
    None,
    None
)
media_related_to_sentence_1.img_attribute_embedding \
    = media_related_to_sentence_1.img_description_embedding \
    = test_input_dict["media_related_to_sentence_1_embedding"]
media_related_to_sentence_1.content_index = 0


def fetch_text_media_input():
    return {
        "sentence_1": sentence_1,
        "sentence_2": sentence_2,
        "media_related_to_sentence_1": media_related_to_sentence_1,
        "media_related_to_sentence_2": media_related_to_sentence_2
    }
