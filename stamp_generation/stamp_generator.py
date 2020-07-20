"""This script creates the Stamp Generator class which is used
to generate the final stamp from the stamp_pages list
received from summarizer"""

import os

from jinja2 import Environment, FileSystemLoader

ABSOLUTE_PATH = os.path.abspath(os.path.dirname(__file__))
RELATIVE_PATH = '/stamp_templates'
STAMP_TEMPLATE_DIRECTORY = ABSOLUTE_PATH + RELATIVE_PATH


class StampGenerator:
    """This helps in creation of stamp_pages"""

    def __init__(self, _website, stamp_pages, enable_animations):
        self._website = _website
        self.stamp_pages = stamp_pages
        self.enable_animations = enable_animations
        self.stamp_html = self.generate_stamp()

    def generate_stamp(self):
        """This method uses jinja2 template(template) and
         renders the output received from summarizer on the template
         and returns rendered template"""

        loader = FileSystemLoader(STAMP_TEMPLATE_DIRECTORY)
        jinja_env = Environment(loader=loader)
        template = jinja_env.get_template('stamp_base_template.jj2')

        return template.render(
            publisher_domain=self._website.domain,
            logo_url=self._website.logo_url,
            canonical_url=self._website.url,
            contents=self._website.contents.content_list,
            pages=self.stamp_pages.stamp_pages,
            title=self._website.get_title(),
            enable_animations=self.enable_animations)
