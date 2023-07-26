#!/usr/bin/env python

import setuptools
import os
import sys

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

setuptools.setup(name='kobo',
    version='0.1',
    description='Markdown Compiler + Server',
    author='Dylan Wallace',
    packages=['kobo'],
    package_dir=package_dir,
    package_data={'kobo': [
        'resources/templates/*',
        'resources/static/css/*',
        'resources/static/js',
        'resources/static/images'
    ]},
    python_requires=">=3.8"
)
