"""This script creates the Stamp Generator class which is used
to generate the final stamp from the stamp_pages list
received from summarizer"""

import logging
import os

from jinja2 import Template

LOGGER = logging.getLogger()

STAMP_DIRECTORY = 'generated_stamp/'
STAMP_TEMPLATE_PATH = 'stamp_generation/stamp_templates/' \
                      'stamp_template.html.jinja'


class StampGenerator:
    """This helps in creation of stamp_pages"""

    def __init__(self, _website, stamp_pages):
        self._website = _website
        self.stamp_pages = stamp_pages
        self.stamp_file_path = self.generate_stamp_file()

    def generate_stamp_file(self):
        """This method returns the path to generated stamp file"""

        template = Template(open(STAMP_TEMPLATE_PATH).read())

        stamp_file \
            = self._website.get_title().replace(" ", "_") + '_stamp.html'

        self.__render_and_save(template, stamp_file)

        return STAMP_DIRECTORY + stamp_file

    def __render_and_save(self, template, stamp_file):
        """This method uses jinja2 template(template) and
         renders the output received from summarizer on the template
         and saves rendered template into stamp file"""

        # generated amp-html stamp code will be saved in stamp_file
        try:
            os.makedirs(STAMP_DIRECTORY, exist_ok=True)
            f = open(STAMP_DIRECTORY + stamp_file, 'w')
            f.write(template.render(
                publisher_domain=self._website.domain,
                logo_url=self._website.logo_url,
                canonical_url=self._website.url,
                contents=self._website.contents.content_list,
                pages=self.stamp_pages.stamp_pages))
            f.close()
        except (IOError, OSError) as err:
            LOGGER.error(err)
