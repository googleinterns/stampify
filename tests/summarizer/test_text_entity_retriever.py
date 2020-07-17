import json
from unittest.mock import Mock, patch

import pytest

from error import BadRequestError
from summarization.text_entity_detection import TextEntityRetriever


def mocked_requests_post(*args, **kwargs):
    json_data = json.loads(kwargs['data'])
    name = ""
    entity_type = ""
    status_code = 200
    if json_data["document"]["content"] == "Sundar Pichai":
        name = "Sundar Pichai"
        entity_type = "PERSON"
    elif json_data["document"]["content"] == "Google":
        name = "Google"
        entity_type = "ORGANIZATION"
    elif json_data["document"]["content"] == "uncategorized entity":
        name = "uncategorized entity"
        entity_type = "OTHER"
    elif json_data["document"]["content"] == "not an entity":
        return Mock(status_code=200, content=json.dumps({
            "entities": []
        }))
    else:
        status_code = 400

    response = json.dumps({
        "entities": [
            {
                "name": name,
                "type": entity_type
            }
        ]
    })

    return Mock(status_code=status_code, content=response)


@patch(
    'summarization.text_entity_detection.requests.post',
    side_effect=mocked_requests_post)
def test_text_entity_retriever_request_format(mocked_post):
    text_entity_retriever = TextEntityRetriever()
    text_entity_retriever._ready_data_for_post_request("Sundar Pichai")
    request_data = json.loads(text_entity_retriever.json_data_for_post_request)
    assert isinstance(request_data, dict)
    assert "document" in request_data
    assert isinstance(request_data["document"], dict)
    assert "content" in request_data["document"]
    assert isinstance(request_data["document"]["content"], str)
    assert "type" in request_data["document"]
    assert isinstance(request_data["document"]["type"], str)
    assert "encodingType" in request_data
    assert request_data["encodingType"] == 1


@patch(
    'summarization.text_entity_detection.requests.post',
    side_effect=mocked_requests_post)
def test_text_entity_retriever_on_person_entity(mocked_post):
    text_entity_retriever = TextEntityRetriever()
    entity_list = text_entity_retriever.get_entities_from_text(
        "Sundar Pichai"
    )
    assert entity_list == ["Sundar Pichai"]


@patch(
    'summarization.text_entity_detection.requests.post',
    side_effect=mocked_requests_post)
def test_text_entity_retriever_on_organization_entity(mocked_post):
    text_entity_retriever = TextEntityRetriever()
    entity_list = text_entity_retriever.get_entities_from_text(
        "Google"
    )
    assert entity_list == ["Google"]


@patch(
    'summarization.text_entity_detection.requests.post',
    side_effect=mocked_requests_post)
def test_text_entity_retriever_on_other_entity(mocked_post):
    text_entity_retriever = TextEntityRetriever()
    entity_list = text_entity_retriever.get_entities_from_text(
        "uncategorized entity"
    )
    assert entity_list == []


@patch(
    'summarization.text_entity_detection.requests.post',
    side_effect=mocked_requests_post)
def test_text_entity_retriever_on_no_entity(mocked_post):
    text_entity_retriever = TextEntityRetriever()
    entity_list = text_entity_retriever.get_entities_from_text(
        "not an entity"
    )
    assert entity_list == []


@patch(
    'summarization.text_entity_detection.requests.post',
    side_effect=mocked_requests_post)
def test_text_entity_retriever_bad_request_throws_error(mocked_post):
    with pytest.raises(BadRequestError) as error:
        text_entity_retriever = TextEntityRetriever()
        text_entity_retriever.get_entities_from_text("")
        assert error.message \
            == "The API call was unsuccessful with response code: 400"
