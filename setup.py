#!/usr/bin/env python3
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright 2017 - Dario Ostuni <dario.ostuni@gmail.com>

import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="terry-cli",
    version="0.0.1",
    author="Dario Ostuni",
    author_email="dario.ostuni@gmail.com",
    description="CLI for creating packages for programming contests",
    license="MPL-2.0",
    keywords="informatics contests italy",
    url="",
    packages=find_packages(),
    long_description=read("README.md"),
    classifiers=[
        "Environment :: Console",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Natural Language :: English", "Operating System :: POSIX",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Scientific/Engineering"
    ],
    entry_points={
        "console_scripts": ["terry = terry_cli.main:main"]
    })
