"""This script contains helper utilities for extractors"""


def get_media_size(node):
    """Returns the size of the video frame"""

    if node.has_attr('width') and node.has_attr('height'):
        return int(node['width']), int(node['height'])
    return 0, 0
