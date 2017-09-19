#!/usr/bin/env python3

from collections import namedtuple
from sys import argv, exit, stderr
import json

from checker_util import parse, PARSED, INVALID, EvaluationOutput, sanitize

if len(argv) != 3:
    print("Usage: %s input_file output_file" % argv[0], file=stderr)
    exit(1)

task_input = open(argv[1], "r")
human_output = open(argv[2], "r")

# reading input file and generating correct output
N = int(task_input.readline())
correct_output = [(int(x.split()[0]) + int(x.split()[1])) for x in task_input]
assert len(correct_output) == N

# evaluating the user's output
def evaluate(num, output):
    """
    Evaluate an output
    @param num: number (1-based) of the testcase to evaluate
    @param output: list with the lines of the output
    @returns an EvaluationOutput object
    """
    try:
        res = int(output[0])
        if res == correct_output[num-1]:
            return EvaluationOutput(status=PARSED, correct=True)
        else:
            return EvaluationOutput(status=PARSED, correct=False)
    except:
        return EvaluationOutput(status=INVALID, validation="Cannot parse number at case #%d: %s" % (num, sanitize(output[0])))

result = parse(human_output.readlines(), N, evaluate, multiline=False)

# printing the json result to stdout
print(json.dumps(result, indent=4))
