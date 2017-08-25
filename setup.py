# This file is part of eventjet-tools.
#
# Eventjet-tools is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# eventjet-tools is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# eventjet-tools. If not, see <http://www.gnu.org/licenses/>.
#
#
# Copyright (C)
#   2017 Alexander Haase <ahaase@alexhaase.de>
#

import os

from setuptools import setup


def read(path):
    """
    Read the contents of a file.


    :param str path: Path to be read.
    :return: The contents of path.
    :rtype: str
    """
    return open(os.path.join(os.path.dirname(__file__), path)).read()


setup(
    name='eventjet',
    description='scripts to process data from Eventjet',
    long_description=read('README.md'),
    author='Alexander Haase',
    author_email='ahaase@alexhaase.de',
    license="GPLv3+",
    url='https://github.com/alehaa/eventjet-tools',

    classifiers=[
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 or later ' +
        '(GPLv3+)',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Utilities',
    ],

    python_requires='>= 3.4',
    install_requires=[],
    setup_requires=[
        'vcversioner',
    ],

    vcversioner={
        'version_module_paths': ['eventjet/_version.py'],
    },


    packages=['eventjet'],
)
