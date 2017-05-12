#!/usr/bin/env python3
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright 2017 - Dario Ostuni <dario.ostuni@gmail.com>

from .c import C
from .cxx import Cxx
from .rust import Rust
from .python import Python
from .utils import get_extension, system_extension

LANGUAGES = [C, Cxx, Rust, Python]
