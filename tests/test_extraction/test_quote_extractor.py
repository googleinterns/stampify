"""
    This script is for unit testing of quote extractor
    Use pytest to run this script
    Command to run: /stampify$ python -m pytest
"""
import pytest

from data_models.quote import Quote
from extraction.content_extractors import quote_extractor
from tests.test_extraction import unit_test_utils as test_utils

__EXTRACTOR = quote_extractor.QuoteExtractor()

__soup = test_utils.soup('quote.html')

expected_output_1 = Quote('This is a quote tag!', 'citation1')

expected_output_2 = Quote('This is another quote tag!', None)


acceptable_test_data = [(__soup.find('q', class_='q_tag1'),
                         expected_output_1),
                        (__soup.find('q', class_='q_tag2'),
                         expected_output_2), ]

non_acceptable_test_data = [(__soup.find('q', class_='q_tag3'), None),
                            (__soup.find('img'), None), ]


@pytest.mark.parametrize("input_node, expected", acceptable_test_data)
def test_tag_should_return_quote_object(input_node, expected):
    actual_quote_content = __EXTRACTOR.validate_and_extract(input_node)

    __assert_quote(actual_quote_content, expected)


@pytest.mark.parametrize("input_node, expected", non_acceptable_test_data)
def test_tag_should_return_none(input_node, expected):
    actual_pinterest_pin_content = __EXTRACTOR.validate_and_extract(input_node)
    assert actual_pinterest_pin_content is expected


def __assert_quote(actual_quote, expected_quote):
    """This is custom assert to compare actual and
       expected quote content"""

    assert isinstance(actual_quote, Quote)
    assert actual_quote.q_content == expected_quote.q_content
    assert actual_quote.cite == expected_quote.cite
