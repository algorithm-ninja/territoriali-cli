#!/usr/bin/env python3
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright 2017 - Dario Ostuni <dario.ostuni@gmail.com>

from sys import argv
from .language_manager import LanguageManager
from .task import Task

def main():
    language_manager = LanguageManager()
    assert len(argv) == 2
    task = Task(argv[1], language_manager)
    task.test_solutions()

if __name__ == "__main__":
    main()
