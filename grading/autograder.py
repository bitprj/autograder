import json
from client.api import assignment
from client.cli.common import messages
import os
import sys

CONFIG_NAME = 'config.ok'
TEST_NAME = 'test.py'


def validate_files(file_names):
    for file_name in file_names:
        # test whether file can be read
        try:
            open(file_name, 'r').close()
        except:
            print("INVALID FILE: " + file_name)
            exit(1)


def create_config(src_names, test_names):
    tests = {TEST_NAME: "ok_test"}

    data = {
        "name": CONFIG_NAME,  # can be anything
        "src": src_names,
        "tests": tests
    }

    # write to file
    with open(CONFIG_NAME, 'w') as f:
        json.dump(data, f, indent=4)


def create_test(src_names, test_names):
    cases = []

    # create cases
    for test_name in test_names:
        with open(test_name, 'r') as f:
            code = f.read()

        cases.append({"code": code})

    setup = "".join(f">>> from {name[:-3]} import *\n" for name in src_names)

    data = {
        "name": TEST_NAME,
        "points": 1,
        "suites": [{
            "cases": cases,
            "setup": setup,
            "type": "doctest"
        }]
    }

    # write to file
    with open(TEST_NAME, 'w') as f:
        f.write('test = ')
        json.dump(data, f, indent=4)


# create config and test files necessary for ok to run
def create_ok_files(src_names, test_names):
    validate_files(src_names)
    validate_files(test_names)

    create_test(src_names, test_names)
    create_config(src_names, test_names)


def grade(src_names, test_names):

    # create config and test files required by ok
    create_ok_files(src_names, test_names)

    args = assignment.Settings(
        verbose=True,  # prints out ALL tests but only sends JSON results up to first fail
        config=CONFIG_NAME# config file to use
    )

    r, w = os.pipe()

    # parent
    if os.fork() > 0:
        # wait for child to finish
        childProcExitInfo = os.wait()
        
        # read grading results from child
        os.close(w)
        r = os.fdopen(r)
        data = r.read()
        r.close()
        return data
    
    # child
    os.close(r)

    # fork because this ignores subsequent submissions
    assign = assignment.load_assignment(args.config, args)

    os.dup2(w, 1) # stdout goes to w
    msgs = messages.Messages()
    for name, proto in assign.protocol_map.items():
        if name == 'grading':  # only run grading protocol
            proto.run(msgs)
    os._exit(1)
