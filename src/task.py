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
        self.compile()

    def compile(self):
        print("Compiling sources for task \"" + self.conf["name"] + "\"", sep='')
        for filename in self.managers:
            print(self.managers[filename])
            self.manager.compile(self.managers[filename])
        for filename in self.solutions:
            print(filename)
            self.manager.compile(filename)

    def _execute_generator(self, input_filename, seed=42, param=0):
        (return_code, output) = self.manager.execute(self.managers["generator"], [str(seed), str(param)])
        assert return_code == 0
        input_file = open(input_filename, "w")
        input_file.write(output.decode())
        input_file.close()
        return output

    def _execute_validator(self, input_string, param=0):
        if "validator" not in self.managers:
            return
        (pipe_read, pipe_write) = os.pipe()
        os.write(pipe_write, input_string)
        os.close(pipe_write)
        return_code = self.manager.execute(self.managers["validator"], [str(param)], pipe_read)[0]
        assert return_code == 0

    def _execute_solution(self, solution_filename, input_string, output_filename):
        (pipe_read, pipe_write) = os.pipe()
        os.write(pipe_write, input_string)
        os.close(pipe_write)
        output = self.manager.execute(solution_filename, [], pipe_read)[1].decode()
        output_file = open(output_filename, "w")
        output_file.write(output)
        output_file.close()

    def _execute_checker(self, input_filename, output_filename):
        (return_code, output) = self.manager.execute(self.managers["checker"], [input_filename, output_filename])
        assert return_code == 0
        return json.loads(output)

    def _generate_tmp_filename(self, kind):
        return gettempdir() + "/__tmp_" + kind + "_terry." + str(getpid())

    def _test_solution(self, solution_filename):
        print("Testing ", solution_filename, " - ", sep='', end='', flush=True)
        tmp_input_name = self._generate_tmp_filename("input")
        tmp_output_name = self._generate_tmp_filename("output")
        input_text = self._execute_generator(tmp_input_name)
        self._execute_validator(input_text)
        self._execute_solution(solution_filename, input_text, tmp_output_name)
        result = self._execute_checker(tmp_input_name, tmp_output_name)
        if result["status"] != 0:
            print("malformed")
        else:
            print(str(result["score"] * self.conf["max_score"]) + " points")
        os.remove(tmp_input_name)
        os.remove(tmp_output_name)

    def test_solutions(self):
        print("Running tests for task \"" + self.conf["name"] + "\"", sep='')
        for filename in self.solutions:
            self._test_solution(filename)
