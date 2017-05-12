#!/usr/bin/env python3
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright 2017 - Dario Ostuni <dario.ostuni@gmail.com>

from .language import Language
from .utils import execute

class Python(Language):
    @staticmethod
    def name():
        return "Python"

    @staticmethod
    def extensions():
        return [".py"]

    @staticmethod
    def execute(executable, args, stdin):
        return execute("python3", [executable] + args, stdin)
