#!/usr/bin/env python3
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright 2017 - Dario Ostuni <dario.ostuni@gmail.com>

import os

from .language import Language
from .utils import execute, system_extension


class Python(Language):
    @staticmethod
    def name():
        return "Python"

    @staticmethod
    def extensions():
        return [".py"]

    @staticmethod
    def compile(source, remove_ext):
        if not remove_ext:
            output = source + system_extension()
        else:
            output = os.path.splitext(source)[0] + system_extension()
        with open(source, "rb") as source_file:
            assert source_file.read(2) == b'#!'
        execute("cp", [source, output])
        execute("chmod", ["+x", output])
        if 'x86_64' in output:
            i686_output = output.replace('x86_64', 'i686')
            execute("cp", [source, i686_output])
            execute("chmod", ["+x", i686_output])
        return output
