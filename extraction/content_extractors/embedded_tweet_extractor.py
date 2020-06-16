"""This script checks whether DOM has embedded tweet tag or not and
creates and returns the ETweet object"""

import bs4

from data_models.embedded_tweet import ETweet
from extraction.interface_content_extractor import IContentExtractor


class ETweetExtractor(IContentExtractor):
    """This class inherits IContentExtractor for extracting embedded tweets"""

    def validate_and_extract(self, node: bs4.element):
        if isinstance(node, bs4.element.Tag) \
                and node.has_attr('class') \
                and ('twitter-tweet' in node['class']
                     or 'twitter-tweet-rendered' in node['class']):

            tweet_a_tag = node.find_all('a')

            if tweet_a_tag and tweet_a_tag[-1].has_attr('href'):
                tweet_url = tweet_a_tag[-1]['href']
                tweet_id = tweet_url.split('/')[-1].split('?')[0]
                return ETweet(tweet_id)

        return None
