"""This script creates CLI to start the program"""

import argparse
import logging

from error import Error
from stampifier import Stampifier

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

    _stampifier = Stampifier(url, maximum_pages)

    try:
        generated_stamp = _stampifier.stampify()
        print(generated_stamp)
    except Error as err:
        LOGGER.debug(err.message)
