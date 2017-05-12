#!/usr/bin/env python3

from sys import argv, exit
import json

assert len(argv) - 1 == 2

task_input = open(argv[1], "r")
human_output = open(argv[2], "r")

n = int(task_input.readline())

correct_output = [(int(x.split()[0]) + int(x.split()[1])) for x in task_input]

assert len(correct_output) == n

case_status = [2 for i in range(n)]
reports = {}

def malformed_exit(why=""):
    result = {}
    result["status"] = 1
    result["why"] = why
    result["score"] = 0.0
    print(json.dumps(result))
    exit(0)

for line in human_output:
    if line[:6] != "Case #":
        malformed_exit("Wrong start of line")
    line = line[6:]
    line = line.split(":")
    if len(line) < 2:
        malformed_exit("Missing case number")
    try:
        case_number = int(line[0])
    except:
        malformed_exit("Invalid case number")
    if case_number < 0 or case_number >= n:
        malformed_exit("Invalid case number")
    line = "".join(line[1:])
    if line[0] != " ":
        malformed_exit("Missing space after column")
    line = line[1:]
    if case_status[case_number] != 2:
        malformed_exit("Repeated case #" + str(case_number))
    line = line.split(" ")
    if len(line) != 1:
        case_status[case_number] = 1
        reports[case_number] = "Not 1 item"
        continue
    try:
        a = int(line[0])
    except:
        case_status[case_number] = 1
        reports[case_number] = "Not a number"
        continue
    if a == correct_output[case_number]:
        case_status[case_number] = 0
    else:
        case_status[case_number] = 1
        reports[case_number] = "Wrong Answer"

result = {}
result["status"] = 0
result["score"] = sum([1 for x in case_status if x == 0]) / float(n)
result["report"] = reports
print(json.dumps(result))
