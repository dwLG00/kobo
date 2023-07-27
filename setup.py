#!/usr/bin/env python

VERSION = '0.1.2'

import setuptools
import os
import sys
import pathlib


package_dir = {'': 'src'}

PACKAGE_DIR = pathlib.Path(__file__).parent
README = (PACKAGE_DIR / 'README.md').read_text()

setuptools.setup(
    name='kobo-md',
    version=VERSION,
    description='Markdown Compiler + Server',
    long_description=README,
    long_description_content_type='text/markdown',
    author='Dylan Wallace',
    packages=['kobo'],
    package_dir=package_dir,
    package_data={'kobo': [
        'resources/templates/*',
        'resources/static/css/*',
        'resources/static/js',
        'resources/static/images',
        'resources/content/*'
    ]},
    python_requires=">=3.8",
    install_requires=[
        'flask',
        'bs4',
        'markdown',
        'markdown-katex'
    ]
)
