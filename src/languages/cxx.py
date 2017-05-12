#!/usr/bin/env python3
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright 2017 - Dario Ostuni <dario.ostuni@gmail.com>

from .language import Language
from .utils import system_extension, execute

class Cxx(Language):
    @staticmethod
    def name():
        return "C++"

    @staticmethod
    def extensions():
        return [".cpp", ".cc", ".cxx", ".c++"]

    @staticmethod
    def compile(source):
        output = source + system_extension()
        execute("g++", ["-o", output, "-std=c++14", "-O2", source])
        return output
