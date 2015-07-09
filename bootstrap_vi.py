from __future__ import print_function

import subprocess
import sys

PYPI_URL = 'https://pypi.python.org/packages/source/v/virtualenv/virtualenv-{VER}.tar.gz'

def get_venv_args(argv):
    '''
    Get only the args for virtualenv
    '''

def download_virtualenv(version=None):
    '''
    Download virtualenv package from pypi

    :param str version: version to download or latest version if None
    '''

def create_virtualenv(venvpath, venvargs=None):
    '''
    Run virtualenv from downloaded venvpath using venvargs
    If venvargs is None, then 'venv' will be used as the virtualenv directory

    :param str venvpath: Path to root downloaded virtualenv package(must contain
        virtualenv.py)
    :param list venvargs: Virtualenv arguments to pass to virtualenv.py
    '''

def bootstrap_vi(version=None, venvargs=None):
    '''
    Bootstrap virtualenv into current directory

    :param str version: Virtualenv version like 13.1.0 or None for latest version
    :param list venvargs: argv list for virtualenv.py or None for default
    '''
