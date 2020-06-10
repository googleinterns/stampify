"""This script is used to scrape data from URL, extract data from the DOM
    and store the extracted data."""

import re

import requests
from bs4 import BeautifulSoup, Comment
from extraction.data_models import contents, text

REQUEST_SESSION = requests.Session()
pattern_for_video_ext = re.compile(r'^.*\.(mp4|ogg|mov|webm)')
pattern_for_ads = re.compile('(^ad-|^ads-)')
extra_tags = ['script', 'noscript', 'style', 'header',
              'footer', 'meta', 'link']


class Extractor:
    """This class takes the URL and extracts the data(DOM) from it using
    Beautiful Soup and stores the extracted data in contents_list"""

    def __init__(self, url):
        self.url = url
        self.soup = None
        self.contents_list = contents.Contents()

    def extract_html(self):
        """This function parses data from HTML using Beautiful Soup"""

        file = REQUEST_SESSION.get(self.url).text    # To request Html from URL

        # Remove the comment to read local files for testing purpose
        # file = open('./test_html.html','r').read()

        self.soup = BeautifulSoup(file, 'lxml')
        self.clean_soup()

        self.__extract_data_from_html()

    def clean_soup(self):
        """This function decomposes the unnecessary data"""

        decomposable_tags = self.soup.find_all(extra_tags)
        comments = self.soup.\
            find_all(text=lambda text: isinstance(text, Comment))
        ads = self.soup.find_all(re.compile('.*'), {'class': pattern_for_ads})

        _ = [comment.extract() for comment in comments]
        _ = [tag.decompose() for tag in decomposable_tags]
        _ = [ad.decompose() for ad in ads]

    def __extract_data_from_html(self):
        """Calls separate functions for extracting data
           from head and body of html"""

        # Extract data from head
        head = self.soup.find('head')
        self.__extract_data_from_html_head(head)

        # Extract data from body
        body_soup = self.soup.find('body')
        self.__extract_data_from_html_body(body_soup)

    def __extract_data_from_html_head(self, soup_head):
        """This function extracts title of HTML"""

        title = soup_head.title
        text_string = title.get_text()
        _content = text.Text(text_string, 'title')
        self.contents_list.add_content(_content)

    def __extract_data_from_html_body(self, node):
        """This function iterates over dom using dfs"""

        is_content, _content = self.__is_content(node)

        # Add to the final list if a valid content is extracted
        if is_content:
            self.contents_list.add_content(_content)

        if node and node.name and not is_content:
            for child in node.contents:
                self.__extract_data_from_html_body(child)

    def __is_content(self, node):
        """This function will extract valid content and return it"""

        # This function will be updated in next iteration
        _ = node
        _ = self.soup

        return False, {}
