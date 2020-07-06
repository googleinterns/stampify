'''
    Install dependencies after installing requirements.txt
'''
from os import system
from ssl import \
    _create_default_https_context  # pylint: disable=unused-import # noqa
from ssl import _create_unverified_context

import nltk


def redownload_nltk_after_ssl_context_update():
    '''
        Python 3.6 on MacOS uses an embedded version of OpenSSL,
        which does not use the system certificate store.
    '''
    try:
        _create_unverified_https_context = _create_unverified_context
    except AttributeError:
        pass
    else:
        _create_default_https_context = _create_unverified_https_context  # noqa
    nltk.download()


if __name__ == '__main__':
    try:
        nltk.download('punkt')
    finally:
        redownload_nltk_after_ssl_context_update()

    system("python3 -m spacy download en_core_web_sm")
