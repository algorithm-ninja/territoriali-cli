#!/usr/bin/env python3
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright 2017 - Dario Ostuni <dario.ostuni@gmail.com>

from .utils import execute, system_extension


class Language():
    @staticmethod
    def name():
        """Return the name of the language"""
        raise NotImplementedError("Implement this method")

    @staticmethod
    def extensions():
        """Return a list of supported extensions"""
        raise NotImplementedError("Implement this method")

    @staticmethod
    def compile(source, remove_ext):
        """Compile the source (if necessary) and return the name of the output"""
        return source

    @staticmethod
    def execute(executable, args, stdin):
        """Execute the program with the given arguments"""
        return execute(executable + system_extension(), args, stdin)
