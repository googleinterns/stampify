"""
    This script is for unit testing of text_extractor
    Use pytest to run this script
    Command to run: /stampify$ python -m pytest
"""
import pytest

from data_models.text import Text
from extraction.content_extractors.text_extractor import TextExtractor
from tests.test_extraction import unit_test_utils as test_utils

__EXTRACTOR = TextExtractor()


__soup = test_utils.soup('text.html')

expected_output_1 = Text('This is paragraph tag.', 'p', is_bold=None)

expected_output_2 = Text('Important Tag!', 'h1', is_bold=None)

expected_output_3 = Text('This is paragraph which is having strong content.',
                         'p', is_bold=True)

expected_output_4 = Text('This is Navigable String.', '', is_bold=None)

acceptable_test_data = [(__soup.find('p', class_='p1'),
                         expected_output_1),
                        (__soup.find('h1'),
                         expected_output_2),
                        (__soup.find('p', class_='p2'),
                         expected_output_3)]

non_acceptable_test_data = [(__soup.find('p', class_='p3'), None),
                            (__soup.find('img'), None)]


@pytest.mark.parametrize("input_node, expected", acceptable_test_data)
def test_tag_should_return_text_object(input_node, expected):
    actual_text_content = __EXTRACTOR.validate_and_extract(input_node)

    __assert_text(actual_text_content, expected)


@pytest.mark.parametrize("input_node, expected", non_acceptable_test_data)
def test_tag_should_return_none(input_node, expected):
    actual_text_content = __EXTRACTOR.validate_and_extract(input_node)
    assert actual_text_content is expected


def __assert_text(actual_text, expected_text):
    """This is custom assert to compare actual and
       expected text content"""

    assert isinstance(actual_text, Text)
    assert actual_text.text_string == expected_text.text_string
    assert actual_text.type == expected_text.type
    assert actual_text.is_bold == expected_text.is_bold
    assert actual_text.font_style == expected_text.font_style
