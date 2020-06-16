"""
    This script is for unit testing of extraction utilities
    Use pytest to run this script
    Command to run: /stampify$ python -m pytest
"""

from extraction.utils import media_extraction_utils as utils


def test_has_domain_should_return_true():
    url = 'https://instagram.com/xyz'
    regex = r'^https://instagram\.com/'

    assert utils.has_domain(url, regex) is not None


def test_has_domain_should_return_false():
    url = 'https://random_website.com/xyz'
    regex = r'^https://instagram\.com/'
    assert utils.has_domain(url, regex) is None
