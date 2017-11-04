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
alerts = []
line_counter = -1

for line in human_output:
    line_counter += 1
    if line[:6] != "Case #":
        alerts.append({
            "severity":
            "warning",
            "message":
            "Line #" + str(line_counter) + " does not start with Case #"
        })
        continue
    line = line[6:]
    line = line.split(":")
    if len(line) < 2:
        alerts.append({
            "severity":
            "warning",
            "message":
            "Cannot parse Case # at line #" + str(line_counter)
        })
        continue
    try:
        case_number = int(line[0])
    except:
        alerts.append({
            "severity": "warning",
            "message": "Invalid Case # at line #" + str(line_counter)
        })
        continue
    if case_number < 0 or case_number >= n:
        alerts.append({
            "severity":
            "warning",
            "message":
            "Case # out of range at line #" + str(line_counter)
        })
        continue
    line = "".join(line[1:])
    if line[0] != " ":
        alerts.append({
            "severity":
            "warning",
            "message":
            "Missing space after colon at line #" + str(line_counter)
        })
        continue
    line = line[1:]
    if case_status[case_number] != 2:
        case_status[case_number] = 1
        reports[case_number] = "multiple Case # definition"
        continue
    line = line.split(" ")
    if len(line) != 1:
        case_status[case_number] = 1
        reports[case_number] = "more than one item given"
        continue
    try:
        a = int(line[0])
    except:
        case_status[case_number] = 1
        reports[case_number] = "not a number"
        continue
    if a == correct_output[case_number]:
        case_status[case_number] = 0
    else:
        case_status[case_number] = -1

output = {
    "validation": {
        "cases": [],
        "alerts": alerts
    },
    "feedback": {
        "cases": [],
        "alerts": []
    }
}
output["score"] = sum([1 for x in case_status if x == 0]) / float(n)
for i in range(n):
    if case_status[i] == -1:
        output["validation"]["cases"].append({"status": "parsed"})
        output["feedback"]["cases"].append({"correct": False})
    elif case_status[i] == 0:
        output["validation"]["cases"].append({"status": "parsed"})
        output["feedback"]["cases"].append({"correct": True})
    elif case_status[i] == 1:
        output["validation"]["cases"].append({
            "status": "invalid",
            "message": reports[i]
        })
        output["feedback"]["cases"].append({"correct": False})
    elif case_status[i] == 2:
        output["validation"]["cases"].append({"status": "missing"})
        output["feedback"]["cases"].append({"correct": False})
    else:
        assert False

print(json.dumps(output))
