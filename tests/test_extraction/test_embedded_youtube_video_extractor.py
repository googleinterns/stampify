"""
    This script is for unit testing of embedded youtube video
    Use pytest to run this script
    Command to run: /stampify$ python -m pytest
"""
import pytest

from extraction.content_extractors import embedded_youtube_video_extractor
from extraction.data_models.embedded_youtube_video import EYouTubeVideo
from tests.test_extraction import unit_test_utils as test_utils

__EXTRACTOR = embedded_youtube_video_extractor.EYouTubeVideoExtractor()

__soup = test_utils.soup('youtube_video.html')

expected_output_1 = EYouTubeVideo("tgbNymZ7vqY", 0, 0)

acceptable_test_data = [(__soup.find('iframe', class_='iframe1'),
                         expected_output_1), ]

non_acceptable_test_data = [(__soup.find('iframe', class_='iframe2'), None),
                            (__soup.find('iframe', class_='iframe3'), None),
                            (__soup.find('p'), None), ]


@pytest.mark.parametrize("input_node, expected", acceptable_test_data)
def test_tag_should_return_eyoutube_video_object(input_node, expected):
    actual_yt_video_content = __EXTRACTOR.validate_and_extract(input_node)

    __assert_youtube_video(actual_yt_video_content, expected)


@pytest.mark.parametrize("input_node, expected", non_acceptable_test_data)
def test_tag_should_return_none(input_node, expected):
    actual_yt_video_content = __EXTRACTOR.validate_and_extract(input_node)
    assert actual_yt_video_content is expected


def __assert_youtube_video(actual_yt_video_content,
                           expected_yt_video_content):
    assert isinstance(actual_yt_video_content, EYouTubeVideo)
    assert actual_yt_video_content.yt_video_id \
           == expected_yt_video_content.yt_video_id
    assert actual_yt_video_content.width \
           == expected_yt_video_content.width
    assert actual_yt_video_content.height \
           == expected_yt_video_content.height
