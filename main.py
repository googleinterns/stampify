"""This script starts the program"""

import argparse
from pprint import pprint

from extraction import extractor


def get_user_input():
    parser = argparse.ArgumentParser(description='Stampify the webpage')
    parser.add_argument('url', type=str, nargs=1,
                        help='An URL of the webpage to stampify.')
    parser.add_argument('page_count', type=int, nargs='?', default=['8'],
                        help='Maximum number of stamp pages to generate.')
    parser.add_argument('-g', action='store_true',
                        help='Generate Stamp')

    args = parser.parse_args()
    url = args.url[0]
    max_pages = args.page_count[0]

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
    URL, maximum_pages = get_user_input()
    extractor = extractor.Extractor(URL)
    extractor.extract_html()
    pprint(extractor.contents_list.get_formatted_list())
