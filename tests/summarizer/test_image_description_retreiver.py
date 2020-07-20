import json
from unittest.mock import Mock, patch

import pytest

from error.stampifier_error import BadRequestError
from summarization.web_entity_detection import ImageDescriptionRetriever


def mocked_requests_post(*args, **kwargs):
    json_data = json.loads(kwargs["data"])
    label = ""
    entity = ""
    has_caption = False
    status_code = 200
    color_num = None
    if json_data["requests"][0]["image"]["source"]["imageUri"] \
            == "http://tinyurl.com/y7how2rj":
        label = "sundar pichai"
        entity = "sundar pichai Alphabet"
        has_caption = True
        color_num = 0

    elif json_data["requests"][0]["image"]["source"]["imageUri"] \
            == "http://tinyurl.com/y9bvoehm":
        label = "larry page"
        entity = "larry page google"
        color_num = 1

    elif json_data["requests"][0]["image"]["source"]["imageUri"] \
            == "http://tinyurl.com/y9t35t3z":
        label = "sergey brin"
        entity = "sergey brin google"
        color_num = 2
    elif json_data["requests"][0]["image"]["source"]["imageUri"] \
            == "img_url_with_no_image_color_annotation":
        color_num = None
    else:
        status_code = 400
        response = {"error": "some error occured"}

    response_dict = {
        "responses": [
            {
                "webDetection": {
                    "webEntities": [
                        {
                            "description": entity
                        }
                    ],
                    "bestGuessLabels": [
                        {
                            "label": label,
                            "languageCode": "en"
                        }
                    ]
                },
                "imagePropertiesAnnotation": {
                    "dominantColors": {
                        "colors": [
                            {
                                "color": {
                                    "red": color_num,
                                    "green": color_num,
                                    "blue": color_num
                                }
                            },
                            {
                                "color": {
                                    "red": color_num,
                                    "green": color_num,
                                    "blue": color_num
                                }
                            },
                            {
                                "color": {
                                    "red": color_num,
                                    "green": color_num,
                                    "blue": color_num
                                }
                            }
                        ]
                    }
                }
            }
        ]
    }

    if has_caption:
        response_dict["responses"][0]["textAnnotation"] = [
            {
                "description":
                    '''this is a sentence that will be detected as a caption
                     and it has to have at least fifteen words or tokens'''
            }
        ]

    if color_num is None:
        response_dict["responses"][0].pop("imagePropertiesAnnotation")

    response = json.dumps(response_dict)

    return Mock(status_code=status_code, content=response)


@patch(
    "summarization.web_entity_detection.requests.post",
    side_effect=mocked_requests_post)
def test_request_format(mocked_post):
    image_describer = ImageDescriptionRetriever(1)
    formatted_request = image_describer._format_single_request("url")

    assert isinstance(formatted_request, dict)

    assert "image" in formatted_request
    assert isinstance(formatted_request["image"], dict)
    assert "source" in formatted_request["image"]
    assert isinstance(formatted_request["image"]["source"], dict)
    assert "imageUri" in formatted_request["image"]["source"]
    assert formatted_request["image"]["source"]["imageUri"] == "url"

    assert "features" in formatted_request
    assert isinstance(formatted_request["features"], list)
    assert isinstance(formatted_request["features"][0], dict)
    assert "maxResults" in formatted_request["features"][0]
    assert "type" in formatted_request["features"][0]
    assert formatted_request["features"][0]["type"] == "WEB_DETECTION"

    assert "type" in formatted_request["features"][1]
    assert formatted_request["features"][1]["type"] == "TEXT_DETECTION"

    assert "type" in formatted_request["features"][2]
    assert formatted_request["features"][2]["type"] == "IMAGE_PROPERTIES"

    assert "imageContext" in formatted_request
    assert isinstance(formatted_request["imageContext"], dict)
    assert "webDetectionParams" in formatted_request["imageContext"]
    assert isinstance(
        formatted_request["imageContext"]["webDetectionParams"], dict)
    assert "includeGeoResults" \
        in formatted_request["imageContext"]["webDetectionParams"]
    assert \
        formatted_request["imageContext"][
            "webDetectionParams"]["includeGeoResults"] \
        == "true"


@ patch(
    "summarization.web_entity_detection.requests.post",
    side_effect=mocked_requests_post)
def test_web_entity_detection(mocked_post):
    image_describer = ImageDescriptionRetriever(1)

    reponse_for_image_url_1 = image_describer.get_description_for_images(
        ["https://tinyurl.com/y7how2rj"])[0]
    assert "sundar pichai" in reponse_for_image_url_1["label"]
    assert "sundar pichai Alphabet" in reponse_for_image_url_1["entities"]
    assert reponse_for_image_url_1["has_caption"]
    assert reponse_for_image_url_1["image_colors"] == [(0, 0, 0)] * 3

    reponse_for_image_url_2 = image_describer.get_description_for_images(
        ["https://tinyurl.com/y9bvoehm"])[0]
    assert "larry page" in reponse_for_image_url_2["label"]
    assert "larry page google" in reponse_for_image_url_2["entities"]
    assert not reponse_for_image_url_2["has_caption"]
    assert reponse_for_image_url_2["image_colors"] == [(1, 1, 1)] * 3

    reponse_for_image_url_3 = image_describer.get_description_for_images(
        ["https://tinyurl.com/y9t35t3z"])[0]
    assert "sergey brin" in reponse_for_image_url_3["label"]
    assert "sergey brin google" in reponse_for_image_url_3["entities"]
    assert not reponse_for_image_url_3["has_caption"]
    assert reponse_for_image_url_3["image_colors"] == [(2, 2, 2)] * 3


@ patch(
    "summarization.web_entity_detection.requests.post",
    side_effect=mocked_requests_post)
def test_bad_request(mocked_post):
    image_describer = ImageDescriptionRetriever(1)
    with pytest.raises(BadRequestError) as error:
        image_describer.get_description_for_images(["bad_url"])
        assert error.message \
            == "The API call was unsuccessful with response code: 400"


def test_url_batch_splitting_for_multiple_of_batch_size():
    image_describer = ImageDescriptionRetriever(3)
    num_batches = 5
    image_describer.image_urls = [
        "url" for i in range(num_batches * image_describer.BATCH_SIZE)
    ]
    image_describer._split_into_batches()
    batch_split_urls = image_describer.image_url_batches

    assert len(batch_split_urls) == num_batches
    for batch in batch_split_urls:
        assert len(batch) == image_describer.BATCH_SIZE


def test_url_batch_splitting_for_multiple_of_batch_size_minus_one():
    image_describer = ImageDescriptionRetriever(3)
    num_batches = 5
    image_describer.image_urls = [
        "url" for i in range(num_batches * image_describer.BATCH_SIZE - 1)
    ]
    image_describer._split_into_batches()
    batch_split_urls = image_describer.image_url_batches

    assert len(batch_split_urls) == num_batches
    for batch_index in range(num_batches):
        if batch_index == num_batches - 1:
            assert len(batch_split_urls[batch_index]
                       ) == image_describer.BATCH_SIZE - 1
        else:
            assert len(batch_split_urls[batch_index]
                       ) == image_describer.BATCH_SIZE


def test_url_batch_splitting_for_multiple_of_batch_size_plus_one():
    image_describer = ImageDescriptionRetriever(3)
    num_batches = 5
    image_describer.image_urls = [
        "url" for i in range(num_batches * image_describer.BATCH_SIZE + 1)
    ]
    image_describer._split_into_batches()
    batch_split_urls = image_describer.image_url_batches

    assert len(batch_split_urls) == num_batches + 1
    for batch_index in range(num_batches + 1):
        if batch_index == num_batches:
            assert len(batch_split_urls[batch_index]) == 1
        else:
            assert len(batch_split_urls[batch_index]
                       ) == image_describer.BATCH_SIZE


def test_request_ordering():
    image_describer = ImageDescriptionRetriever(3)
    image_describer.all_responses_list = list()
    image_describer.all_responses_list.extend(
        [(1, ["one"]), (0, ["zero"]), (2, ["two"])]
    )
    assert image_describer._get_ordered_and_combined_request_responses() == \
        ["zero", "one", "two"]


@ patch(
    "summarization.web_entity_detection.requests.post",
    side_effect=mocked_requests_post)
def test_request_number(mocked_post):
    image_describer = ImageDescriptionRetriever(1)

    actual_request_number = 1

    returned_request_number, _ = image_describer._make_post_request(
        ["https://tinyurl.com/y9t35t3z"],
        actual_request_number
    )

    assert actual_request_number == returned_request_number


@ patch(
    "summarization.web_entity_detection.requests.post",
    side_effect=mocked_requests_post)
def test_default_response_with_no_colors(mocked_post):
    image_describer = ImageDescriptionRetriever(1)

    image_response = image_describer.get_description_for_images(
        ["img_url_with_no_image_color_annotation"]
    )[0]

    assert image_response["image_colors"] == [(-1, -1, -1)]
