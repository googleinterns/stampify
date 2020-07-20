"""This script contains helper utilities for stampify"""
import validators


def valid_url(url):
    """Adds necessary fix and validates URL"""

    if url.startswith('//'):
        url = 'http:{}'.format(url)

    if validators.url(url):
        return url

    return None
