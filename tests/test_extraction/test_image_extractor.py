"""
    This script is for unit testing of image_extractor
    Use pytest to run this script
    Command to run: /stampify$ python -m pytest
"""
import bs4
import pytest

from extraction import image_extractor
from extraction.data_models.image import Image

__EXTRACTOR = image_extractor.ImageExtractor()


def soup():
    """Returns soup from html file"""
    __test_file = open('./tests/test_extraction/image.html')
    __test_file_data = __test_file.read()
    __test_file.close()
    return bs4.BeautifulSoup(__test_file_data, 'lxml')


expected_output_1 = Image('image_with_src_and_title.jpg',
                          100, 100, False, None,
                          'This is Image with src and title!', '')

expected_output_2 = Image('image_with_src_but_without_title.gif',
                          0, 0, True, None, None, '')

expected_output_3 = Image('image_with_src_and_title_inside_figure.jpg',
                          0, 0, False, None,
                          'This is Image with src and title inside figure!',
                          '')

expected_output_4 = Image('image_with_src_but_without_title_inside_figure.jpg',
                          100, 100, False, 'This is figcaption.',
                          None, '')

acceptable_test_data = [(soup().find('img', class_='img1'),
                         expected_output_1),
                        (soup().find('img', class_='img2'),
                         expected_output_2),
                        (soup().find('figure', class_='fig1'),
                         expected_output_3),
                        (soup().find('figure', class_='fig2'),
                         expected_output_4), ]

non_acceptable_test_data = [(soup().find('img', class_='img3'), None),
                            (soup().find('figure', class_='fig3'), None),
                            (soup().find('figure', class_='fig4'), None),
                            (soup().find('h1'), None)]


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
