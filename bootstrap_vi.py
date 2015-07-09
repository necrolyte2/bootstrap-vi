from __future__ import print_function

import subprocess
import sys
import re
from os.path import join, basename

try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen

try:
    from __builtin__ import open
except ImportError:
    from builtins import open

PYPI_DL_URL = 'https://pypi.python.org/packages/source/v/virtualenv/virtualenv-{VER}.tar.gz'
PYPI_VI_URL = 'https://pypi.python.org/pypi/virtualenv'

class VersionError(Exception):
    '''
    Generic error fetching version
    '''
    pass

def get_venv_args(argv):
    '''
    Get only the args for virtualenv
    '''
    if not argv:
        return []
    if argv[0] == '-':
        return argv[1:]
    elif argv[0] == __name__+'.py':
        return argv[1:]
    return argv

def get_latest_virtualenv_version():
    '''
    Fetch pypi page for virtualenv and parse out latest version

    :return str: version string(Ex. 13.1.0)
    '''
    data = urlopen(PYPI_VI_URL).read()
    if isinstance(data, bytes):
        html = data.decode('utf-8')
    else:
        html = data
    m = re.search('virtualenv (\d+\.\d+\.\d+)', html)
    if not m:
        raise VersionError("Cannot get latest version from PYPI")
    return m.group(1)

def download_virtualenv(version, dldir=None):
    '''
    Download virtualenv package from pypi and return response that can be
    read and written to file

    :param str version: version to download or latest version if None
    :param str dldir: directory to download into or None for cwd
    '''
    dl_url = PYPI_DL_URL.format(VER=version)
    filename = basename(dl_url)
    if dldir:
        dl_path = join(dldir, filename)
    else:
        dl_path = filename
    data = urlopen(PYPI_DL_URL.format(VER=version))
    with open(dl_path, 'wb') as fh:
        fh.write(data.read())
    return dl_path

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
