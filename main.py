"""
This script creates CLI to start the program

Command to run this script:

$python3 main.py 'https://www.scoopwhoop.com/
                  entertainment/memes-from-dd-ramayan/' 5
$python3 main.py 'https://www.scoopwhoop.com/
                  entertainment/memes-from-dd-ramayan/'

For more help: python3 main.py -h
"""

import argparse
import logging
import os

from error import Error
from stampifier import Stampifier

LOGGER = logging.getLogger()
LOG_FILENAME = 'website.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

STAMP_DIRECTORY = 'output/'
HTML_EXTENSION = '.html'


def get_user_input():
    """This method implements Command Line Interface"""

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

    _url, maximum_pages = get_user_input()

    _stampifier = Stampifier(_url, maximum_pages)

    try:
        stampifier_output = _stampifier.stampify()

        stamp_file = stampifier_output.stamp_title.replace(' ', '_') \
            + HTML_EXTENSION

        if stampifier_output.stamp_html:
            # Save the generated_stamp to file
            os.makedirs(STAMP_DIRECTORY, exist_ok=True)
            f = open(STAMP_DIRECTORY + stamp_file, 'w')
            f.write(stampifier_output.stamp_html)
            f.close()
    except Error as err:
        LOGGER.debug(err.message)
    except (IOError, OSError) as err:
        LOGGER.debug(err)
