"""
    This script is for unit testing of image_extractor
    Use pytest to run this script
    Command to run: /stampify$ python -m pytest
"""
import pytest

from data_models.image import Image
from extraction.content_extractors import image_extractor
from tests.test_extraction import unit_test_utils as test_utils

__EXTRACTOR = image_extractor.ImageExtractor()

__soup = test_utils.soup('image.html')

expected_output_1 = Image('http://www.google.com/'
                          'image_with_src_and_title.jpg',
                          100, 100, False, None,
                          'This is Image with src and title!', '')

expected_output_2 = Image('http://www.google.com/'
                          'image_with_src_but_without_title.gif',
                          0, 0, True, None, None, '')

expected_output_3 = Image('http://www.google.com/'
                          'image_with_src_and_title_inside_figure.jpg',
                          0, 0, False, None,
                          'This is Image with src and title inside figure!',
                          '')

expected_output_4 = Image('http://www.google.com/'
                          'image_with_src_but_without_title_inside_figure.jpg',
                          100, 100, False, 'This is figcaption.',
                          None, '')

expected_output_5 = Image('http://www.google.com/image7.jpg',
                          0, 0, False, None,
                          'This url is valid after fix', '')


acceptable_test_data = [(__soup.find('img', class_='img1'),
                         expected_output_1),
                        (__soup.find('img', class_='img2'),
                         expected_output_2),
                        (__soup.find('figure', class_='fig1'),
                         expected_output_3),
                        (__soup.find('figure', class_='fig2'),
                         expected_output_4),
                        (__soup.find('img', class_='img7'),
                         expected_output_5)]

non_acceptable_test_data = [(__soup.find('img', class_='img3'), None),
                            (__soup.find('figure', class_='fig3'), None),
                            (__soup.find('figure', class_='fig4'), None),
                            (__soup.find('h1'), None),
                            (__soup.find('img', class_='img8'), None)]


@pytest.mark.parametrize("input_node, expected", acceptable_test_data)
def test_img_tag_should_return_image_object(input_node, expected):
    actual_image_content = __EXTRACTOR.validate_and_extract(input_node)

    __assert_image(actual_image_content, expected)


@pytest.mark.parametrize("input_node, expected", non_acceptable_test_data)
def test_tag_should_return_none(input_node, expected):
    actual_image_content = __EXTRACTOR.validate_and_extract(input_node)
    assert actual_image_content is expected


def __assert_image(actual_image, expected_image):
    """This is custom assert to compare actual and
       expected image content"""

    assert isinstance(actual_image, Image)
    assert actual_image.img_url == expected_image.img_url
    assert actual_image.img_width == expected_image.img_width
    assert actual_image.img_height == expected_image.img_height
    assert actual_image.img_title == expected_image.img_title
    assert actual_image.img_caption == expected_image.img_caption
    assert actual_image.img_type == expected_image.img_type
    assert actual_image.is_gif == expected_image.is_gif
