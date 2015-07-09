from setuptools import setup, find_packages

setup(
    name = 'bootstrap_vi',
    version = '0.0.1',
    packages = find_packages(),
    install_requires = [],
    author = 'Tyghe Vallard',
    author_email = 'vallardt@gmail.com',
    description = 'Bootstrap virtualenv without pip or easy_install',
    license = 'MIT',
    keywords = 'bootstrap, virtualenv',
    url = 'https://github.com/necrolyte2/bootstrap_vi',
    entry_points = {
        'console_scripts': [
        ]
    },
    setup_requires = [
        'nose',
        'mock',
        'unittest2',
        'tempdir'
    ]
)
