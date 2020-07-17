"""Script to start the server for Stampify"""

import logging
import os
from urllib.parse import urlunparse

from flask import Flask, render_template, request

from error import StampifierError
from stampifier import Stampifier

app = Flask(__name__, static_folder='assets/')
app.secret_key = os.environ['FLASK_APP_SECRET_KEY']

LOGGER = logging.getLogger()
LOG_FILENAME = 'website.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

DEFAULT_STORY = 'https://preview.amp.dev/documentation/' \
                'examples/introduction/stories_in_amp/'


@app.route('/')
def home():
    """Renders the home page for Stampify"""
    # Add a default stampified page here. For now using placeholder story.
    url = ""
    max_pages = "4"
    enable_animations = False
    if 'website_url' in request.args:
        url = request.args.get('website_url')
    if 'max_pages' in request.args:
        max_pages = request.args.get('max_pages')
    if 'animations' in request.args:
        enable_animations = request.args.get('animations')

    scheme, netloc, params, fragments = '', '', '', ''
    path = '/stampified_url'
    query = 'url={}&max_pages={}&animations={}'.format(
                                     url, max_pages, enable_animations)

    stampified_url = urlunparse((scheme, netloc, path,
                                 params, query, fragments)) \
        if url else DEFAULT_STORY

    return render_template('index.html',
                           url=url, max_pages=max_pages,
                           stampified_url=stampified_url)


@app.route('/stampified_url', methods=['GET'])
def stampify_url():
    """The stampified version of the URL passed in args."""

    url = request.args.get('url')
    max_pages = request.args.get('max_pages')
    enable_animations = request.args.get('animations')

    _stampifier = Stampifier(url, int(max_pages), enable_animations)

    try:
        return _stampifier.stampify().stamp_html
    except StampifierError as err:
        return render_template('error_screen.html',
                               message=err.message)
