"""This script checks whether DOM has image tag or not and
creates and returns the Image object"""

import bs4

from data_models.image import Image
from extraction.content_extractors.interface_content_extractor import \
    IContentExtractor
from extraction.utils import media_extraction_utils as utils
from utils import url_utils


class ImageExtractor(IContentExtractor):
    """This class inherits IContentExtractor to extract Images"""

    def validate_and_extract(self, node: bs4.element):
        if node.name == 'img' and node.has_attr('src'):
            return self.__create_image(node)
        if node.name == 'figure':
            img_tag = node.find('img')
            if img_tag and img_tag.has_attr('src'):
                return self.__create_image(img_tag, node.find('figcaption'))

        return None

    def __create_image(self, node, caption_tag=None):
        """This method extracts all attributes for the image
        and creates Image object instance"""

        # Prioritizing data-src if present for extracting URL over src
        # as src is used as lazy loading when data-src is present.

        if node.has_attr('data-src'):
            image_url = node['data-src']
        else:
            image_url = node['src']

        image_url = url_utils.valid_url(image_url)
        if not image_url:
            return None

        image_title, image_caption = None, None
        if node.has_attr('title'):
            image_title = node['title']

        image_height, image_width = utils.get_media_size(node)
        is_image_gif = image_url.endswith('.gif')

        if caption_tag:
            image_caption = caption_tag.get_text()

        return Image(image_url,
                     image_height,
                     image_width,
                     is_image_gif,
                     img_caption=image_caption,
                     img_title=image_title)
