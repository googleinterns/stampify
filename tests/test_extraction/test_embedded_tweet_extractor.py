"""
    This script is for unit testing of embedded_tweet_extractor
    Use pytest to run this script
    Command to run: /stampify$ python -m pytest
"""
import pytest

from data_models.embedded_tweet import ETweet
from extraction.content_extractors import embedded_tweet_extractor
from tests.test_extraction import unit_test_utils as test_utils

__EXTRACTOR = embedded_tweet_extractor.ETweetExtractor()

__soup = test_utils.soup('embedded_tweet.html')

expected_output_1 = ETweet('123456789123456789')

expected_output_2 = ETweet('987654321987654321')

acceptable_test_data \
    = [(__soup.find('blockquote', class_='twitter-tweet'),
        expected_output_1),
       (__soup.find('blockquote', class_='twitter-tweet-rendered'),
        expected_output_2), ]

non_acceptable_test_data = [(__soup.find('p', class_='twitter-tweet'), None),
                            (__soup.find('p', class_='p1'), None), ]


@pytest.mark.parametrize("input_node, expected", acceptable_test_data)
def test_tag_should_return_etweet_object(input_node, expected):
    actual_tweet_content = __EXTRACTOR.validate_and_extract(input_node)

    __assert_tweet(actual_tweet_content, expected)


@pytest.mark.parametrize("input_node, expected", non_acceptable_test_data)
def test_tag_should_return_none(input_node, expected):
    actual_tweet_content = __EXTRACTOR.validate_and_extract(input_node)
    assert actual_tweet_content is expected


def __assert_tweet(actual_tweet_content, expected_tweet_content):
    """Custom assert to compare actual and expected tweet content"""

    assert isinstance(actual_tweet_content, ETweet)
    assert actual_tweet_content.tweet_id == expected_tweet_content.tweet_id
