import os
from os.path import join, exists

import unittest2 as unittest
import tempdir
import mock

# Normalize python2 and python3 errors
try:
    from urllib2 import HTTPError, URLError
except ImportError:
    from urllib.error import HTTPError, URLError

# Python 3 FileNotFoundError same as Python2 IOError.errno 2
try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError

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

class TestCreateVirtualenv(unittest.TestCase):
    def setUp(self):
        self.patch_subprocess = mock.patch.object(bootstrap_vi, 'subprocess')
        self.mock_subprocess = self.patch_subprocess.start()
        self.addCleanup(self.mock_subprocess.stop)

    def test_runs_virtualenv_without_args_default_venv_dir(self):
        r = bootstrap_vi.create_virtualenv('virtualenvpath')
        self.mock_subprocess.Popen.assert_called_once_with(
            ['virtualenvpath/virtualenv.py', 'venv']
        )
        self.mock_subprocess.Popen.return_value.communicate.assert_called_once_with()

    def test_runs_virtualenv_with_args_path(self):
        args = ['--prompt', '"(bar)"', 'foo']
        r = bootstrap_vi.create_virtualenv('virtualenvpath', args)
        self.mock_subprocess.Popen.assert_called_once_with(
            ['virtualenvpath/virtualenv.py'] + args
        )
        self.mock_subprocess.Popen.return_value.communicate.assert_called_once_with()

class TestBootstrapVi(unittest.TestCase):
    def setUp(self):
        self.tdir = tempdir.TempDir()
        os.chdir(self.tdir.name)
        self.patch_sys = mock.patch.object(bootstrap_vi, 'sys')
        self.mock_sys = self.patch_sys.start()
        self.addCleanup(self.patch_sys.stop)

    def tearDown(self):
        os.chdir('/')

    def test_creates_latest_virtualenv_defaults_run_normal(self):
        self.mock_sys.argv = ['bootstrap_vi.py']
        bootstrap_vi.main()
        self.assertTrue(exists('venv/bin/activate'), 'Did not create venv/bin/activate')

    def test_creates_latest_virtualenv_defaults_run_from_pipe(self):
        self.mock_sys.argv = []
        bootstrap_vi.main()
        self.assertTrue(exists('venv/bin/activate'), 'Did not create venv/bin/activate')

    def test_creates_virtualenv_with_args_run_from_pipe(self):
        self.mock_sys.argv = ['-', 'vpath', '--prompt', 'findpromptfind']
        self.latest_ver = bootstrap_vi.get_latest_virtualenv_version()
        bootstrap_vi.main()
        with open('vpath/bin/activate') as fh:
            self.assertIn('findpromptfind', fh.read())
