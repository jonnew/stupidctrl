try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Synchronize recordings of multiple client programs.',
    'author': 'Jon Newman',
    'url': 'https://github.com/jonnew/stupidctrl',
    'author_email': 'jpnewman snail mit dot edu',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['stupidctrl'],
    'scripts': [],
    'name': 'stupidctrl'
}

setup(**config)
