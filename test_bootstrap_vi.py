import os
from os.path import join

import unittest2 as unittest

try:
    from urllib2 import HTTPError, URLError
except ImportError:
    from urllib.error import HTTPError, URLError

# Python 3 FileNotFoundError same as Python2 IOError.errno 2
try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError

import mock

import bootstrap_vi

class TestGetVenvArgs(unittest.TestCase):
    def test_strips_beginning_dash(self):
        args = ['-', 'venv']
        r = bootstrap_vi.get_venv_args(args)
        self.assertEqual(args[1:], r)

    def test_strips_beginning_dash_if_exists(self):
        args = ['venv']
        r = bootstrap_vi.get_venv_args(args)
        self.assertEqual(args, r)

    def test_returns_empty_list_if_empty_argv(self):
        r = bootstrap_vi.get_venv_args([])
        self.assertEqual([], r)
        r = bootstrap_vi.get_venv_args(None)
        self.assertEqual([], r)
        r = bootstrap_vi.get_venv_args(['bootstrap_vi.py'])
        self.assertEqual([], r)

    def test_returns_args_after_scriptname(self):
        args = ['bootstrap_vi.py', 'venv']
        r = bootstrap_vi.get_venv_args(args)
        self.assertEqual(['venv'], r)

class PatchUrlopen(unittest.TestCase):
    def setUp(self):
        self.url_patch = mock.patch.object(bootstrap_vi, 'urlopen')
        self.mock_urlopen = self.url_patch.start()
        self.addCleanup(self.url_patch.stop)

class TestGetLastestVirtualenvVersion(PatchUrlopen):
    def test_gets_correct_version(self):
        self.mock_urlopen.return_value.read.return_value = \
            '<html><h1>virtualenv 13.1.0</h1></html>'
        r = bootstrap_vi.get_latest_virtualenv_version()
        self.assertEqual('13.1.0', r)
        self.mock_urlopen.assert_called_once_with(
            bootstrap_vi.PYPI_VI_URL
        )
        self.mock_urlopen.return_value.read.assert_called_once_with()

    def test_version_cannot_be_found(self):
        self.mock_urlopen.return_value.read.return_value = '<html></html>'
        self.assertRaises(
            bootstrap_vi.VersionError,
            bootstrap_vi.get_latest_virtualenv_version
        )

    def test_read_urlopen_read_returns_bytes(self):
        try:
            html = bytes('<html><h1>virtualenv 13.1.0</h1></html>', 'utf-8')
        except TypeError:
            html = bytes('<html><h1>virtualenv 13.1.0</h1></html>')
        self.mock_urlopen.return_value.read.return_value = html
        r = bootstrap_vi.get_latest_virtualenv_version()
        self.assertEqual('13.1.0', r)
        
class TestDownloadVirtualenv(PatchUrlopen):
    def test_version_supplied_does_not_exist(self):
        self.mock_urlopen.side_effect = HTTPError(
            'https://www.foo.com', 404, 'Missing', '', open(os.devnull)
        )
        self.assertRaises(
            HTTPError,
            bootstrap_vi.download_virtualenv, '100.0.0'
        )

    def test_dldir_does_not_exist_raises_exception(self):
        self.assertRaises(
            FileNotFoundError,
            bootstrap_vi.download_virtualenv, '13.1.0', '/missingpath/'
        )

    def test_creates_downloaded_file(self):
        with mock.patch.object(bootstrap_vi, 'open') as mock_open:
            r = bootstrap_vi.download_virtualenv('13.1.0', '/tmp')
            mock_open.assert_called_once_with('/tmp/virtualenv-13.1.0.tar.gz', 'wb')
            self.assertEqual(
                1,
                mock_open.return_value.__enter__.return_value.write.call_count
            )
            self.assertEqual('/tmp/virtualenv-13.1.0.tar.gz', r)
            self.mock_urlopen.assert_called_once_with(
                bootstrap_vi.PYPI_DL_URL.format(VER='13.1.0')
            )
            self.mock_urlopen.return_value.read.assert_called_once_with()
