"""
    This script is for unit testing of embedded_instagram_post_extractor
    Use pytest to run this script
    Command to run: /stampify$ python -m pytest
"""
import bs4
import pytest

from extraction import embedded_instagram_post_extractor
from extraction.data_models.embedded_instagram_post import EInstagramPost

__EXTRACTOR = embedded_instagram_post_extractor.EInstagramPostExtractor()


def soup():
    """Returns soup from html file"""
    __test_file = open('./tests/test_extraction/instagram.html')
    __test_file_data = __test_file.read()
    __test_file.close()
    return bs4.BeautifulSoup(__test_file_data, 'lxml')


__soup = soup()

expected_output_1 = EInstagramPost("post_shortcode1", '')

expected_output_2 = EInstagramPost("post_shortcode2", '')

expected_output_3 = EInstagramPost("short_code1", '')

acceptable_test_data = [(__soup.find('blockquote', class_='node1'),
                         expected_output_1),
                        (__soup.find('blockquote', class_='node2'),
                         expected_output_2),
                        (__soup.find('iframe', class_='iframe1'),
                         expected_output_3), ]

non_acceptable_test_data = [(soup().find('div').get_text(), None),
                            (soup().find('p'), None),
                            (soup().find('iframe', class_='iframe2'), None),
                            (soup().find('iframe', class_='iframe3'), None)]


@pytest.mark.parametrize("input_node, expected", acceptable_test_data)
def test_tag_should_return_einstragram_post_object(input_node, expected):
    actual_instagram_content = __EXTRACTOR.validate_and_extract(input_node)

    __assert_instagram_post(actual_instagram_content, expected)


@pytest.mark.parametrize("input_node, expected", non_acceptable_test_data)
def test_tag_should_return_none(input_node, expected):
    actual_instagram_content = __EXTRACTOR.validate_and_extract(input_node)
    assert actual_instagram_content is expected


def __assert_instagram_post(actual_instagram_content,
                            expected_instagram_content):
    """This is custom assert to compare actual and
       expected instagram content"""

    assert isinstance(actual_instagram_content, EInstagramPost)
    assert actual_instagram_content.insta_shortcode \
           == expected_instagram_content.insta_shortcode
    assert actual_instagram_content.media_type \
           == expected_instagram_content.media_type
