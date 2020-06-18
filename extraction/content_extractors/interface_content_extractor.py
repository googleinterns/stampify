"""This script creates Interface"""

import bs4


class IContentExtractor:
    """Interface for content extractors"""

    def validate_and_extract(self, node: bs4.element):
        """Extract content from BeautifulSoup tags."""
