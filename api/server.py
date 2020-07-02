"""Script to start the server for Stampify"""

import logging
import os

from flask import Flask, redirect, render_template, request, session, url_for

from error import Error
from stampifier import Stampifier

app = Flask(__name__, static_folder='assets/')
app.secret_key = os.environ['FLASK_APP_SECRET_KEY']

LOGGER = logging.getLogger()
LOG_FILENAME = 'website.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)


@app.route('/')
def home():
    return render_template('index.html', show_options=False)


@app.route('/submit', methods=['POST'])
def convert_to_stamp():
    """Uses the data provided by user via API and
    converts the webpage to STAMP and returns the
    final response to user"""

    url = request.form['website_url']
    max_pages = request.form['max_pages']

    _stampifier = Stampifier(url, int(max_pages))

    try:
        session['stamp'] = _stampifier.stampify()
    except Error as err:
        LOGGER.debug(err.message)

    return redirect(url_for('show_options'))


@app.route('/result')
def show_options():
    return render_template('index.html', show_options=True)


@app.route('/generated_stamp')
def show_stamp():
    return session['stamp']


if __name__ == '__main__':
    app.run()
