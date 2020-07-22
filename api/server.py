"""Script to start the server for Stampify"""

from urllib.parse import urlencode, urlunparse

from flask import Flask, render_template, request

from error.stampifier_error import StampifierError
from stampifier import Stampifier

app = Flask(__name__, static_folder='assets/')

DEFAULT_STORY = 'https://preview.amp.dev/documentation/' \
                'examples/introduction/stories_in_amp/'
DEFAULT_MAX_PAGES = 8


@app.route('/')
def home():
    """Renders the home page for Stampify"""

    url = ""
    max_pages = DEFAULT_MAX_PAGES
    enable_animations = False

    if 'website_url' in request.args:
        url = request.args.get('website_url')
    if 'max_pages' in request.args:
        max_pages = request.args.get('max_pages')
    if 'animations' in request.args:
        enable_animations = request.args.get('animations')

    scheme, netloc, params, fragments = '', '', '', ''
    path = '/stampified_url'
    query = urlencode({'url': url,
                       'max_pages': max_pages,
                       'animations': enable_animations})

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
    enable_animations = bool(request.args.get('animations') == 'on')

    if not max_pages:
        max_pages = DEFAULT_MAX_PAGES

    _stampifier = Stampifier(url, int(max_pages), enable_animations)

    try:
        return _stampifier.stampify().stamp_html
    except StampifierError as err:
        return render_template('error_screen.html',
                               message=err.message)
