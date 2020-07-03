"""This script creates the Stamp Generator class which is used
to generate the final stamp from the stamp_pages list
received from summarizer"""

import logging
import os

from jinja2 import Template

LOGGER = logging.getLogger()

ABSOLUTE_PATH = os.path.abspath(os.path.dirname(__file__))
RELATIVE_PATH = '/stamp_templates/stamp_template.html.jinja'
STAMP_TEMPLATE_PATH = ABSOLUTE_PATH + RELATIVE_PATH


class StampGenerator:
    """This helps in creation of stamp_pages"""

    def __init__(self, _website, stamp_pages):
        self._website = _website
        self.stamp_pages = stamp_pages
        self.stamp_code = self.generate_stamp()

    def generate_stamp(self):
        """This method uses jinja2 template(template) and
         renders the output received from summarizer on the template
         and returns rendered template"""

        template = Template(open(STAMP_TEMPLATE_PATH).read())

        return template.render(
            publisher_domain=self._website.domain,
            logo_url=self._website.logo_url,
            canonical_url=self._website.url,
            contents=self._website.contents.content_list,
            pages=self.stamp_pages.stamp_pages,
            title=self._website.get_title())
