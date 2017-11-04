#!/usr/bin/env python3
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright 2017 - Dario Ostuni <dario.ostuni@gmail.com>

import os

from .language import Language
from .utils import system_extension, execute


class Rust(Language):
    @staticmethod
    def name():
        return "Rust"

    @staticmethod
    def extensions():
        return [".rs"]

    @staticmethod
    def compile(source, remove_ext):
        if not remove_ext:
            output = source + system_extension()
        else:
            output = os.path.splitext(source)[0] + system_extension()
        execute("rustc", ["-o", output, "-O", source])
        if 'x86_64' in output:
            i686_output = output.replace('x86_64', 'i686')
            execute("rustc", [
                "--target", "i686-unknown-linux-gnu", "-o", i686_output, "-O",
                source
            ])
        return output
