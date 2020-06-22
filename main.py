"""This script starts the program"""

import argparse
import logging

from data_models.website import Website
from extraction import extractor

LOGGER = logging.getLogger()
LOG_FILENAME = 'website.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)


def get_user_input():
    parser = argparse.ArgumentParser(description='Stampify the webpage')
    parser.add_argument('url', type=str, nargs=1,
                        help='An URL of the webpage to stampify.')
    parser.add_argument('page_count', type=int, nargs='?', default=8,
                        help='Maximum number of stamp pages to generate.')
    parser.add_argument('-g', action='store_true',
                        help='Generate Stamp')

    args = parser.parse_args()
    url = args.url[0]
    max_pages = args.page_count

    return url, max_pages


def convert_website_to_stamp(_website, maximum_pages):
    """This method can be used the pipeline between all the modules"""

    _ = maximum_pages

    _extractor = extractor.Extractor(_website.url)
    _website.set_contents(_extractor.extract_html())

    LOGGER.debug(_website.__dict__)


if __name__ == '__main__':
    """
      Command to run this script:

      $python3 main.py 'https://www.scoopwhoop.com/
                              entertainment/memes-from-dd-ramayan/' 5
      $python3 main.py 'https://www.scoopwhoop.com/
                              entertainment/memes-from-dd-ramayan/'

      For more help: python3 main.py -h
    """

    url, maximum_pages = get_user_input()

    _website = Website(url)

    if not _website.is_valid:
        LOGGER.error("Invalid URL!")
    else:
        convert_website_to_stamp(_website, maximum_pages)
