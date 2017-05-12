#!/usr/bin/env python3
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright 2017 - Dario Ostuni <dario.ostuni@gmail.com>

from os.path import isdir, splitext
from os import listdir, getpid
from tempfile import gettempdir
import os
import json
from ruamel import yaml
from .languages import system_extension

class Task():
    def __init__(self, directory, manager):
        if directory[-1] != "/":
            directory += "/"
        self.manager = manager
        self.directory = directory
        dirs = ["", "statement", "solutions", "managers"]
        if not all([isdir(directory + "/" + x) for x in dirs]):
            raise Exception(directory + " is missing")
        self.conf = yaml.round_trip_load(open(directory + "/task.yaml", "r").read())
        if not all([x in self.conf for x in ("name", "description", "max_score")]):
            raise Exception(directory + ": something is missing in task.yaml")
        def plain_file(filename):
            return splitext(splitext(filename)[0])[1] + splitext(filename)[1] != system_extension()
        self.managers = {}
        for filename in listdir(directory + "managers/"):
            basename = splitext(filename)[0]
            if not plain_file(filename):
                continue
            if basename == "generator":
                self.managers["generator"] = directory + "managers/" + filename
            elif basename == "checker":
                self.managers["checker"] = directory + "managers/" + filename
            elif basename == "validator":
                self.managers["validator"] = directory + "managers/" + filename
        if not all([x in self.managers for x in ("generator", "validator")]):
            raise Exception(self.conf["name"] + ": something is missing in managers")
        self.solutions = [directory + "solutions/" + x for x in listdir(directory + "solutions/") if plain_file(x)]

    def compile(self):
        print("Compiling sources for task \"" + self.conf["name"] + "\"", sep='')
        for filename in self.managers:
            print(self.managers[filename])
            self.manager.compile(self.managers[filename])
        for filename in self.solutions:
            print(filename)
            self.manager.compile(filename)

    def test_solutions(self):
        self.compile()
        print("Running tests for task \"" + self.conf["name"] + "\"", sep='')
        for filename in self.solutions:
            print("Testing ", filename, " - ", sep='', end='', flush=True)
            tmp_input_name = gettempdir() + "/__tmp_input_terry." + str(getpid())
            tmp_output_name = gettempdir() + "/__tmp_output_terry." + str(getpid())
            (ret, out) = self.manager.execute(self.managers["generator"], ["42", "0"])
            assert ret == 0
            tmp_input = open(tmp_input_name, "w")
            tmp_input.write(out.decode())
            tmp_input.close()
            if "validator" in self.managers:
                (pread, pwrite) = os.pipe()
                os.write(pwrite, out)
                os.close(pwrite)
                (ret, _) = self.manager.execute(self.managers["validator"], ["0"], pread)
                assert ret == 0
            (pread, pwrite) = os.pipe()
            os.write(pwrite, open(tmp_input_name, "rb").read())
            os.close(pwrite)
            (ret, out) = self.manager.execute(filename, [], pread)
            tmp_output = open(tmp_output_name, "w")
            tmp_output.write(out.decode())
            tmp_output.close()
            (ret, out) = self.manager.execute(self.managers["checker"], [tmp_input_name, tmp_output_name])
            assert ret == 0
            result = json.loads(out)
            if result["status"] != 0:
                print("malformed")
            else:
                print(str(result["score"] * self.conf["max_score"]) + " points")
            os.remove(tmp_input_name)
            os.remove(tmp_output_name)
