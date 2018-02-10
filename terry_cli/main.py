#!/usr/bin/env python3
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright 2017 - Dario Ostuni <dario.ostuni@gmail.com>

from sys import argv, exit
import logging, os
from .language_manager import LanguageManager
from .task import Task

def main():
    if len(argv) < 2:
        print("Usage: terry <task_folder>")
        exit(1)

    logging.basicConfig(level=logging.INFO)
    language_manager = LanguageManager()

    os.chdir(argv[1])

    # Delete compiled and/or backup files
    for dirname, _, filenames in os.walk("."):
        for filename in filenames:
            if any(filename.endswith(ext) for ext in {".i686", ".x86_64"}):
                os.remove(os.path.join(dirname, filename))

    task = Task(".", language_manager)
    task.test_solutions()

if __name__ == "__main__":
    main()
