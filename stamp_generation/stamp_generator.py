"""This script creates the Stamp Generator class which is used
to generate the final stamp from the stamp_pages list
received from summarizer"""

from jinja2 import Template


class StampGenerator:
    """This helps in creation of stamp_pages"""

    def __init__(self, _website, stamp_pages):
        self._website = _website
        self.stamp_pages = stamp_pages

    def generate_stamp(self):
        """This method uses jinja2 template(stamp_template.html.jinja) and renders
        the output received from summarizer on the template."""

        template_path = 'stamp_templates/stamp_template.html.jinja'
        template = Template(open(template_path).read())
        return template.render(
            publisher_domain=self._website['domain'],
            logo_url=self._website['logo_url'],
            canonical_url=self._website['url'],
            contents=self._website['contents']['content_list'],
            pages=self.stamp_pages)
