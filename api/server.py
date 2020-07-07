"""Script to start the server for Stampify"""

import logging
import os

from flask import Flask, render_template, request

from error import Error
from stampifier import Stampifier

app = Flask(__name__, static_folder='assets/')
app.secret_key = os.environ['FLASK_APP_SECRET_KEY']

LOGGER = logging.getLogger()
LOG_FILENAME = 'website.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)


@app.route('/')
def home():
    """Renders the home page for Stampify"""
    # Add a default stampified page here. For now using placeholder story.
    url = 'https://www.scoopwhoop.com/news/' \
          'pandemic-importance-of-human-connection-in-socially-distant-world'
    max_pages = 5

    if 'website_url' in request.args:
        url = request.args.get('website_url')
    if 'max_pages' in request.args:
        max_pages = request.args.get('max_pages')

    stampified_url = '/stampified_url?url=%s&max_pages=%s' % (url, max_pages)

    return render_template('index.html', show_options=False,
                           url=url, max_pages=max_pages,
                           stampified_url=stampified_url)


@app.route('/stampified_url', methods=['GET'])
def stampify_url():
    """The stampified version of the URL passed in args."""
    url = request.args.get('url')
    max_pages = request.args.get('max_pages')

    _stampifier = Stampifier(url, int(max_pages))

    try:
        return _stampifier.stampify().stamp_html
    except Error as err:
        return err.message
