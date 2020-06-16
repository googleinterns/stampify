"""
    This script is for unit testing of embedded youtube video
    Use pytest to run this script
    Command to run: /stampify$ python -m pytest
"""
import bs4
import pytest

from extraction import embedded_youtube_video_extractor
from extraction.data_models.embedded_youtube_video import EYouTubeVideo

__EXTRACTOR = embedded_youtube_video_extractor.EYouTubeVideoExtractor()


def soup():
    """Returns soup from html file"""
    __test_file = open('./tests/test_extraction/youtube_video.html')
    __test_file_data = __test_file.read()
    __test_file.close()
    return bs4.BeautifulSoup(__test_file_data, 'lxml')


__soup = soup()

expected_output_1 = EYouTubeVideo("tgbNymZ7vqY", 0, 0)

acceptable_test_data = [(soup().find('iframe', class_='iframe1'),
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
