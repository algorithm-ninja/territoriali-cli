#!/usr/bin/env python3

from sys import argv, exit, stderr
from terry_cli.parser import Parser


if len(argv) != 3:
    print("Usage: %s input_file output_file" % argv[0], file=stderr)
    exit(1)

task_input = open(argv[1], "r")
human_output = open(argv[2], "r")

# reading input file and generating correct output
N = int(task_input.readline())
correct_output = [(int(x.split()[0]) + int(x.split()[1])) for x in task_input]
assert len(correct_output) == N


def evaluate(num, stream):
    out = stream.int()
    stream.end()
    if out == correct_output[num-1]:
        return 1.0
    return 0.0, "nope! %d != %d" % (out, correct_output[num-1])


def evaluate_strict(num, stream):
    stream.space()
    out = stream.int()
    stream.space()
    stream.end()
    if out == correct_output[num-1]:
        return 1.0
    return 0.0, "nope! %d != %d" % (out, correct_output[num-1])

parser = Parser(evaluate, N, human_output, int_max_len=20, strict_spaces=False)
# parser = Parser(evaluate_strict, N, human_output, int_max_len=20, strict_spaces=True)
parser.run()
