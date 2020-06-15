"""
    This script is for unit testing of video_extractor
    Use pytest to run this script
    Command to run: /stampify$ python -m pytest
"""
import bs4
import pytest

from extraction import video_extractor
from extraction.data_models.video import Video

__EXTRACTOR = video_extractor.VideoExtractor()


# TODO: Move to test_utils in next iterations.
def soup():
    """Returns soup from html file"""
    __test_file = open('./tests/test_extraction/video.html')
    __test_file_data = __test_file.read()
    __test_file.close()
    return bs4.BeautifulSoup(__test_file_data, 'lxml')


__soup = soup()

expected_output_1 = Video(['video1.mp4'], 100, 100)

expected_output_2 = Video(['movie1.mp4', 'movie1.ogg'], 320, 240)

expected_output_3 = Video(['movie1.mp4'], 320, 240)

expected_output_4 = Video(['embed_video1.mp4'], 0, 0)

acceptable_test_data = [(__soup.find('video', class_='video_node1'),
                         expected_output_1),
                        (__soup.find('video', class_='video_node2'),
                         expected_output_2),
                        (__soup.find('video', class_='video_node3'),
                         expected_output_3),
                        (__soup.find('embed', class_='embed1'),
                         expected_output_4)]

non_acceptable_test_data = [(__soup.find('video', class_='video_node4'), None),
                            (__soup.find('video', class_='video_node5'), None),
                            (__soup.find('embed', class_='embed2'), None),
                            (__soup.find('embed', class_='embed3'), None),
                            (__soup.find('img'), None)]


@pytest.mark.parametrize("input_node, expected", acceptable_test_data)
def test_tag_should_return_video_object(input_node, expected):
    actual_video_content = __EXTRACTOR.validate_and_extract(input_node)

    __assert_video(actual_video_content, expected)


@pytest.mark.parametrize("input_node, expected", non_acceptable_test_data)
def test_tag_should_return_none(input_node, expected):
    actual_video_content = __EXTRACTOR.validate_and_extract(input_node)
    assert actual_video_content is expected


def __assert_video(actual_video, expected_video):
    """This is custom assert to compare actual and
       expected video content"""

    assert isinstance(actual_video, Video)
    assert actual_video.video_urls == expected_video.video_urls
    assert actual_video.width == expected_video.width
    assert actual_video.height == expected_video.height
