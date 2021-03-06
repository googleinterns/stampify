"""
    This script is for unit testing of embedded
    pinterest_pin extractor

    Use pytest to run this script
    Command to run: /stampify$ python -m pytest
"""
import pytest

from data_models.embedded_pinterest_pin import EPinterestPin
from extraction.content_extractors import embedded_pinterest_pin_extractor
from tests.test_extraction import unit_test_utils as test_utils

__EXTRACTOR = embedded_pinterest_pin_extractor.EPinterestPinExtractor()

__soup = test_utils.soup('pinterest_pin.html')

expected_output_1 \
    = EPinterestPin('https://www.pinterest.com/pin/99360735500167749/')

acceptable_test_data = [(__soup.find('a', class_='a_tag1'),
                         expected_output_1), ]

non_acceptable_test_data = [(__soup.find('a', class_='a_tag2'), None),
                            (__soup.find('a', class_='a_tag3'), None),
                            (__soup.find('a', class_='a_tag4'), None),
                            (__soup.find('img'), None), ]


@pytest.mark.parametrize("input_node, expected", acceptable_test_data)
def test_tag_should_return_epinterestpin_object(input_node, expected):
    actual_pinterest_pin_content = __EXTRACTOR.validate_and_extract(input_node)

    __assert_pinterest_pin(actual_pinterest_pin_content, expected)


@pytest.mark.parametrize("input_node, expected", non_acceptable_test_data)
def test_tag_should_return_none(input_node, expected):
    actual_pinterest_pin_content = __EXTRACTOR.validate_and_extract(input_node)
    assert actual_pinterest_pin_content is expected


def __assert_pinterest_pin(actual_pinterest_pin, expected_pinterest_pin):
    """This is custom assert to compare actual and
       expected pinterest pin content"""

    assert isinstance(actual_pinterest_pin, EPinterestPin)
    assert actual_pinterest_pin.pin_url == expected_pinterest_pin.pin_url
