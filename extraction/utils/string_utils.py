"""This script contains helper utilities for strings"""

HEADING_TAGS = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
TEXT_TAGS = ['p', 'span', 'code'] + HEADING_TAGS
TEXT_MIN_SCORE = 50


def empty_text(_str):
    """Returns true if null string"""
    return not _str.strip()


def is_important_text(node):
    """Returns true if the tag has important text"""

    return not (0 < len(node.get_text()) < TEXT_MIN_SCORE
                and node.name not in HEADING_TAGS)
