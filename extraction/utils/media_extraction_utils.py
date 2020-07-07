"""This script contains helper utilities for extractors"""

import re

import validators


def has_domain(url, regex):
    return re.compile(regex).match(url)


def get_media_size(node):
    """Returns the size of the media content"""

    if node.has_attr('width') and node.has_attr('height'):
        return int(node['width']), int(node['height'])
    return 0, 0


def invalid_url(url):
    """Adds necessary fix and validates image URL"""

    if url.startswith('//'):
        url = 'http:{}'.format(url)

    return not validators.url(url), url
