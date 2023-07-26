#!/usr/bin/env python

VERSION = '0.1.1'

import setuptools
import os
import sys
import pathlib


def project_path(*sub_paths):
    project_dirpath = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(project_dirpath, *sub_paths)


def read(*sub_paths):
    with open(project_path(*sub_paths), mode="rb") as fh:
        return fh.read().decode("utf-8")

package_dir = {'': 'src'}
install_requires = [
    line.strip()
    for line in read('requirements.txt').splitlines()
    if line.strip() and not line.startswith("#")
]

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
    python_requires=">=3.8"
)
