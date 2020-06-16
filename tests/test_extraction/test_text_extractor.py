"""
    This script is for unit testing of text_extractor

    Use pytest to run this script
    Command to run: /stampify$ python -m pytest
"""
import bs4
import pytest

from data_models.text import Text
from extraction.content_extractors import text_extractor
from extraction.utils import string_utils as utils

__EXTRACTOR = text_extractor.TextExtractor()


@pytest.fixture(scope='module')
def soup():
    """Returns soup from html file"""
    __test_file \
        = open('./tests/test_extraction/extraction_test_inputs/text.html')
    __test_file_data = __test_file.read()
    __test_file.close()
    return bs4.BeautifulSoup(__test_file_data, 'lxml')


@pytest.fixture()
def heading_node_1(soup):
    """Returns <h1>Important Tag!</h1>"""
    return soup.find('h1')


@pytest.fixture
def para_node_1(soup):
    """Returns
        <p class="p1">This is paragraph with less than 50 characters.</p>
    """
    return soup.find('p', class_='p1')


@pytest.fixture
def para_node_2(soup):
    """Returns
        <p class="p2">
        This is paragraph which is considered <b>important</b>
        as it has more than 50 characters
        </p>
    """
    return soup.find('p', class_='p2')


@pytest.fixture
def para_node_3(soup):
    """<p class="p3">\n\n\t\n\t    \n\n\t</p>"""
    return soup.find('p', class_='p3')


@pytest.fixture
def nav_string_1(soup):
    """Returns
            '
        This is Navigable String with more than 50 characters.
    '
    """
    return soup.find('div', class_='div1').contents[0]


@pytest.fixture
def nav_string_2(soup):
    """Returns
        '
        This is not important!
    '
    """
    return soup.find('div', class_='div3').contents[0]


@pytest.fixture
def nav_string_3(soup):
    """Returns '\n\n\n\n\n'"""
    return soup.find('div', class_='div3').contents[0]


@pytest.fixture
def img_tag(soup):
    """Returns <img src="image_url.jpg">"""
    return soup.find('img')


# Tests for valid text tags
def test_not_null_bs4_h1_text_tags_with_importance(heading_node_1):
    """This method adds tests for case that should return <Text Object>"""

    actual_text = __EXTRACTOR.validate_and_extract(heading_node_1)

    text_type = 'h1'
    text_string = 'Important Tag!'
    expected_text = Text(text_string, text_type)
    expected_text.font_style = ''

    __assert_text(actual_text, expected_text)


def test_not_null_bs4_p_text_tags_with_importance(para_node_2):
    """This method adds tests for case that should return <Text Object>"""

    actual_text = __EXTRACTOR.validate_and_extract(para_node_2)

    text_type = 'p'
    text_string = 'This is paragraph which ' \
                  'is considered important as ' \
                  'it has more than 50 characters'
    expected_text = Text(text_string, text_type)
    expected_text.font_style = ''

    __assert_text(actual_text, expected_text)


def test_not_null_navigable_string_having_min_text_score(nav_string_1):
    """This method adds tests for case that should return <Text Object>"""

    actual_text = __EXTRACTOR.validate_and_extract(nav_string_1)

    text_type = ''
    text_string = 'This is Navigable String ' \
                  'with more than 50 characters.'
    expected_text = Text(text_string, text_type)
    expected_text.font_style = ''

    __assert_text(actual_text, expected_text)


# Tests for not valid text tags
def test_null_navigable_string(nav_string_3):
    """This method adds tests for case that should return None"""

    text_content = __EXTRACTOR.validate_and_extract(nav_string_3)
    assert text_content is None


def test_not_null_navigable_string_not_having_min_text_score(nav_string_2):
    """This method adds tests for case that should return None"""

    text_content = __EXTRACTOR.validate_and_extract(nav_string_2)
    assert text_content is None


def test_null_bs4_text_tags(para_node_3):
    """This method adds tests for case that should return None"""

    text_content = __EXTRACTOR.validate_and_extract(para_node_3)
    assert text_content is None


def test_not_null_bs4_text_tags_with_no_importance(para_node_1):
    """This method adds tests for case that should return None"""

    text_content = __EXTRACTOR.validate_and_extract(para_node_1)
    assert text_content is None


def test_valid_bs4_tag_but_not_text_tag(img_tag):
    """This method adds tests for case that should return None"""

    text_content = __EXTRACTOR.validate_and_extract(img_tag)
    assert text_content is None


# Tests for string_utils methods
def test_empty_text_returns_true():
    """This method adds test for case when string is empty"""

    test_string = '\n\t  \n'
    assert utils.empty_text(test_string) is True


def test_empty_text_returns_false():
    """This method adds test for case when string is not empty"""

    test_string = 'Not Null String'
    assert utils.empty_text(test_string) is False


def test_is_important_text_returns_true(heading_node_1):
    assert utils.is_important_text(heading_node_1) is True


def test_is_important_text_returns_false(para_node_1):
    assert utils.is_important_text(para_node_1) is False


def __assert_text(actual_text, expected_text):
    """Custom assert to compare actual and expected text output"""

    assert isinstance(actual_text, Text)
    assert actual_text.text_string == expected_text.text_string
    assert actual_text.type == expected_text.type
    assert actual_text.font_style == expected_text.font_style
