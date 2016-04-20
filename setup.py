#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setupi, find_packages
from codecs import open
from os import path

# Get the long description from the README file
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup (
    name = 'stupidctrl',
    description = 'A stupidctrl to synchronize recordings of multiple client programs.',
    author = 'Jon Newman',
    url = 'https =//github.com/jonnew/stupidctrl',
    author_email = 'jpnewman snail mit dot edu',
    version = '1.0.0',
    tests_require = ['nose'],
    install_requires = ['transitions', 'pyzmq'],
    packages=find_packages(),
    scripts = [],
    license = 'Beerware',
    long_description = long_description,

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 2',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],

    entry_points={
        'console_scripts': [
            'stupidctrl = stupidctrl:main',
        ],
    }
)
