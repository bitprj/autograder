from shutil import rmtree
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from zipfile import ZipFile
import json
import os
import re


# Function to edit the input.py file
# Only executes if input.py file is in the zip file
def edit_input(src_names, txt_names):
    input_config_name = 'input.py'

    # check if input configuration file passed in
    if input_config_name in src_names:
        # create filenames array
        filenames_array = "filenames = " + str(txt_names) + "\n"

        # get original contents and adds the filenames array
        with open(input_config_name, 'r') as f:
            contents = f.read()
            contents = filenames_array + contents
            f.close()

        # write-back prepended contents
        with open(input_config_name, 'w') as f:
            f.write(contents)
            f.close()

    return


# Function to extract files from zip files
def extract(name):
    restricted_names = ['autograder.py', 'config.ok', 'test.py']
    with ZipFile(name, 'r') as zip:
        extracted_names = zip.namelist()
        # check if files have reserved names
        bad_names = intersection(restricted_names, extracted_names)
        if bad_names:
            raise (Exception(f"Zipfile cannot contain files named {bad_names}"))

        zip.extractall()

        return extracted_names


# no longer used
def get_case_num(case):
    # First line, get case number at the end
    first_line = case[0]
    case_phrase = "".join(re.findall("Case .*", first_line))
    case_num = case_phrase.split()[-1]
    return case_num


def get_files(src_names, test_names):
    src_file_objs = []
    test_file_objs = []
    for filename in src_names:
        with open(filename, 'r') as f:
            src_file_objs.append(FileStorage(stream=f, filename=filename, content_type='application/x-python-code'))
    for filename in test_names:
        with open(filename, 'r') as f:
            test_file_objs.append(FileStorage(stream=f, filename=filename, content_type='text/plain'))

    return src_file_objs, test_file_objs


def intersection(l1, l2):
    return list(set(l1) & set(l2))


def parseToJSON(results, test_names):
    results = results.split('---------------------------------------------------------------------\n')
    summary = results[-1]
    num_pass, num_fail = parse_summary(summary)

    # a test failed, parse it
    cases = results[1:-1]
    cases = parse_cases(cases, test_names)
    pass_cases, fail_case = cases["pass_cases"], cases["fail_case"]

    if not pass_cases and not fail_case:
        data = {"error": "Please double check your submission"}
    else:
        data = {
            "pass_cases": pass_cases,
            "fail_case": fail_case,
            "num_fail": num_fail,
            "num_pass": num_pass
        }

    return json.loads(json.dumps(data))


def parse_cases(cases, test_names):
    parsed_cases = {
        "pass_cases": [],
        "fail_case": {}
    }
    i = 0
    for case in cases:
        # tokenize case into lines
        case = case.split('\n')
        if case[-3] == '-- OK! --':  # pass
            parsed_cases["pass_cases"].append({
                # "name": "TODO",
                "name": test_names[i],
                "output": case[2:-3]
            })
            i += 1
        else:  # fail
            parsed_cases["fail_case"] = parse_fail(case)
        # if fail_start:
        #    parsed_cases
        # pass_cases = [line for line in case[2:fail_start]][:-3]
        # parsed_cases[case_num] = { "fail_case": fail_case, "pass_cases": pass_cases }
    return parsed_cases


def parse_fail(case):
    try:
        # at least one test failed
        error_start = case.index("# Error: expected")
    except:
        # all tests passed
        return {}

    # get lines detailing expected-output fail
    error_lines = [line for line in case[error_start:] if line.startswith('#')]

    try:
        # divides expected and output
        divide = error_lines.index('# but got')
        expected = []
        output = []

        # parse expected
        for line in error_lines[1:divide]:
            expected.append(line[1:].strip())
        # parse output
        for line in error_lines[divide + 1:]:
            output.append(line[1:].strip())
    except:
        raise (Exception("Could not divide expected and output lines!"))

    return {"name": "TODO", "expected": expected, "output": output}


def parse_summary(summary):
    pass_phrase = "".join(re.findall("Passed: .*\n", summary))
    fail_phrase = "".join(re.findall("Failed: .*\n", summary))

    num_pass = pass_phrase.split()[-1]
    num_fail = fail_phrase.split()[-1]

    return int(num_pass), int(num_fail)


def save_file(zipfile):
    filename = secure_filename(zipfile.filename)
    with open(filename, 'wb') as f:
        zipfile.save(f)
    return filename


# Function to remove files used when testing
def remove_files(filenames):
    if os.path.exists("src.zip"):
        os.remove("src.zip")

    if os.path.isdir("__MACOSX"):
        rmtree("__MACOSX")

    for name in filenames:
        if os.path.exists(name):
            os.remove(name)
    os.remove("tests.zip")
    os.chdir("../")

    return
