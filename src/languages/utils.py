#!/usr/bin/env python3
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright 2017 - Dario Ostuni <dario.ostuni@gmail.com>

import platform
import logging
from subprocess import check_output, CalledProcessError
from os.path import splitext

def system_extension():
    return "." + platform.system().lower() + "." + platform.machine()

def execute(command, args, stdin=None):
    logging.debug([command] + args)
    try:
        return (0, check_output([command] + args, stdin=stdin))
    except CalledProcessError as e:
        return (e.returncode, e.output)
    except Exception as e:
        return (255, e)
    except:
        return (255, "Generic error")


def get_extension(filename):
    return splitext(filename)[1]
