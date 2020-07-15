"""This script contains helper utilities for stampify"""

from urllib.parse import urlparse, urlunparse

import validators


def valid_url(url):
    """Adds necessary fix and validates URL"""

    if url.startswith('//'):
        url = 'http:{}'.format(url)

    if validators.url(url):
        return url

    return None


def convert_scheme_to_http(url):
    """This converts urls scheme from https to http"""

    _url = urlparse(url)
    scheme = 'http' if _url.scheme == 'https' \
        else _url.scheme

    return urlunparse((scheme, ) + _url[1:])
