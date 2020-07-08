"""This script is used to scrape data from URL, extract data from the DOM
    and store the extracted data."""

import logging
import re

import requests
from bs4 import BeautifulSoup, Comment

from data_models import contents, text
from error import (NoneTypeMarkupError, WebsiteConnectionError,
                   WebsiteNotStampifiableError)
from extraction.content_extractors import (embedded_instagram_post_extractor,
                                           embedded_pinterest_pin_extractor,
                                           embedded_tweet_extractor,
                                           embedded_youtube_video_extractor,
                                           image_extractor, quote_extractor,
                                           text_extractor, video_extractor)

LOGGER = logging.getLogger()
REQUEST_SESSION = requests.Session()
CONTENT_EXTRACTORS \
    = (video_extractor.VideoExtractor(),
       text_extractor.TextExtractor(),
       image_extractor.ImageExtractor(),
       embedded_pinterest_pin_extractor.EPinterestPinExtractor(),
       quote_extractor.QuoteExtractor(),
       embedded_tweet_extractor.ETweetExtractor(),
       embedded_youtube_video_extractor.EYouTubeVideoExtractor(),
       embedded_instagram_post_extractor.EInstagramPostExtractor(),)

pattern_for_ads = re.compile('(^ad-|^ads-|ads|ad|Ad|Ads'
                             '|advertisement|Advertisement|'
                             'advertising|Advertising)')

extra_tags = ['script', 'noscript', 'style', 'header',
              'footer', 'meta', 'link', 'nav', 'aside']

KEYWORDS = ['header', 'Header', 'nav', 'Nav',
            'menu', 'Menu', 'side', 'Side',
            'footer', 'Footer', 'subscribe', 'Subscribe',
            'breadcrumb', 'bread-crumb', 'Breadcrumb',
            'comment', 'Comment', 'cmt', 'Cmt',
            'search', 'Search', 'banner',
            'recent', 'Recent', 'author', 'Author',
            'latest', 'Latest', 'you-may', 'trending',
            'Trending', 'share', 'Share', 'social', 'Social',
            'pagination', 'Pagination', 'next', 'Next', 'nxt',
            'related', 'Related', 'home-cards', 'topicArea',
            'tabHide', 'rightSec', 'reststory', 'tags', 'Tags',
            'alsoread', 'also-read', "news_letter_box",
            "cookie", "report-story", "count", "recommended",
            "Recommended", "connect", "Connect", "live", "Live",
            "login", "Login", "sign-up", "signup", "Signup", "fb",
            "notify", "notification", "Notification", "swiper",
            "extra", "Extra", "more", "More", "newsletter",
            "Newsletter", "notice", "Notice", "options", "Options"]


class Extractor:
    """This class takes the URL and extracts the data(DOM) from it using
    Beautiful Soup and stores the extracted data in contents_list"""

    def __init__(self, url):
        self.url = url
        self.contents_list = contents.Contents()
        self.soup = None

    def extract_html(self):
        """This function parses data from HTML using Beautiful Soup"""
        file = None

        try:
            # To request Html from URL
            file = REQUEST_SESSION.get(self.url).text
        except requests.exceptions.ConnectionError:
            raise WebsiteConnectionError(self.url)

        # Remove the comment to read local files for testing purpose
        # file = open('./test_html.html','r').read()

        if not file:
            raise NoneTypeMarkupError()

        self.soup = BeautifulSoup(file, 'lxml')
        self.clean_soup()

        self.__extract_data_from_html()

        if not self.contents_list:
            raise WebsiteNotStampifiableError(
                message="No content extracted!",
                failure_source="Extractor")

        return self.contents_list

    def clean_soup(self):
        """This function decomposes the unnecessary data"""

        decomposable_tags = self.soup.find_all(extra_tags)
        comments = self.soup. \
            find_all(text=lambda text: isinstance(text, Comment))
        ads = self.soup.find_all(class_=pattern_for_ads)

        _ = [comment.extract() for comment in comments]
        _ = [tag.decompose() for tag in decomposable_tags]
        _ = [ad.decompose() for ad in ads]

        for keyword in KEYWORDS:
            _ = [_content.decompose() for _content in
                 self.soup.find_all(
                     class_=re.compile('.*{}.*'.format(keyword)))]
            _ = [_content.decompose() for _content in
                 self.soup.find_all(
                     id=re.compile('.*{}.*'.format(keyword)))]

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

        text_string = ''
        if soup_head.find('title'):
            title = soup_head.title
            text_string = title.get_text()

        self.contents_list.add_content(text.Text(text_string, 'title'))

    def __extract_data_from_html_body(self, node):
        """This function iterates over dom using dfs"""

        _content = self.__validate_and_extract_content(node)

        # Add to the final list if a valid content is extracted
        if _content:
            self.contents_list.add_content(_content)
            return

        if node and node.name:
            for child in node.contents:
                self.__extract_data_from_html_body(child)

    def __validate_and_extract_content(self, node):
        """This function will extract valid content and return it"""

        _ = self.soup

        for content_extractor in CONTENT_EXTRACTORS:
            content = content_extractor.validate_and_extract(node)
            if content:
                return content

        return None
