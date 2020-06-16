"""This is a helper utility for unit testing"""

import bs4


def soup(file_name):
    """Returns soup from html file"""
    __test_file = open('./tests/test_extraction/extraction_test_inputs/'
                       + file_name)
    __test_file_data = __test_file.read()
    __test_file.close()
    return bs4.BeautifulSoup(__test_file_data, 'lxml')
