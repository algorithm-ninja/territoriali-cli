#!/usr/bin/env python3

import re
from collections import namedtuple

MISSING = "missing"
PARSED = "parsed"
INVALID = "invalid"

Alert = namedtuple("Alert", ["severity", "message"])
class EvaluationOutput:
    def __init__(self, status, *, correct=False, score=None, validation=None, feedback=None):
        self.status = status
        self.correct = correct
        self.validation = validation
        self.feedback = feedback
        if score is not None:
            self.score = score
        else:
            self.score = 1.0 if correct == True else 0.0

new_case = re.compile("Case #(\\d+):(.*)$")

def sanitize(output):
    MAX_LEN = 50
    if len(output) < MAX_LEN:
        return output
    return output[:MAX_LEN] + "..."

def parse(lines, num_inputs, evaluate_cb, multiline=False):
    current_number = None
    current_output = []
    used_cases = set()
    skipping = False
    output = {
        "score": 0.0,
        "validation": {
            "cases": [{ "status": MISSING } for _ in range(num_inputs)],
            "alerts": []
        },
        "feedback": {
            "cases": [{ "correct": False } for _ in range(num_inputs)],
            "alerts": []
        }
    }

    def process_result(num, eval_result):
        """Process the output of the evaluation"""
        output["score"] += eval_result.score / float(num_inputs)
        output["validation"]["cases"][num-1]["status"] = eval_result.status
        if eval_result.validation:
            output["validation"]["cases"][num-1]["message"] = eval_result.validation
        output["feedback"]["cases"][num-1]["correct"] = eval_result.correct
        if eval_result.feedback:
            output["feedback"]["cases"][num-1]["message"] = eval_result.feedback

    def add_alert(alert):
        """Append a new alert to the list"""
        output["validation"]["alerts"].append({
            "severity": alert.severity,
            "message": alert.message
        })

    for line_no, line in enumerate(lines, 1):
        # skip all the empty lines
        if len(line.strip()) == 0: continue
        match = new_case.search(line)
        # not a new "Case #%d:"
        if not match:
            if not multiline:
                add_alert(Alert("warning", "Unexpected data at line %d. Keeping only the first line of #%d" % (line_no, current_number)))
                line = "" # skip the line but not break the testcase
            if current_number is None:
                add_alert(Alert("warning", "Expecting new testcase at line %d" % (line_no)))
                skipping = True
            stripped = line.strip()
        # a new testcase
        else:
            # send the last test case if exists
            if not skipping and current_number is not None:
                eval_result = evaluate_cb(current_number, current_output)
                process_result(current_number, eval_result)
            current_number = int(match.group(1))
            current_output = []
            skipping = False
            stripped = match.group(2).strip()

            if current_number in used_cases:
                add_alert(Alert("warning", "Duplicated case #%d at line %d. Skipping." % (current_number, line_no)))
                skipping = True
            if not 1 <= current_number <= num_inputs:
                add_alert(Alert("warning", "Invalid testcase number #%d at line %d" % (current_number, line_no)))
                skipping = True
            used_cases.add(current_number)

        if not skipping and len(stripped) > 0:
            current_output += [stripped]

    # the last testcase may not be evaluated yet
    if not skipping and current_number is not None:
        eval_result = evaluate_cb(current_number, current_output)
        process_result(current_number, eval_result)

    return output
