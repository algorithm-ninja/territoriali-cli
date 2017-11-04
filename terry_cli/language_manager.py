#!/usr/bin/env python3
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright 2017 - Dario Ostuni <dario.ostuni@gmail.com>

from .languages import LANGUAGES, get_extension, Language
from os.path import splitext


class LanguageManager():
    def __init__(self):
        self.exmap = {}
        for language in LANGUAGES:
            for extension in language.extensions():
                self.exmap[extension] = language

    def known(self, source):
        return get_extension(source) in self.exmap

    def compile(self, source, remove_ext=False):
        if not self.known(source):
            return
        return self.exmap[get_extension(source)].compile(source, remove_ext)

    def execute(self, executable, args, stdin=None):
        if not self.known(executable):
            return Language.execute(executable, args, stdin)
        return self.exmap[get_extension(executable)].execute(
            executable, args, stdin)
