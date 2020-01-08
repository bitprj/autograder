import json
import re
from werkzeug import secure_filename
from zipfile import ZipFile

def extract(name):
    restricted_names = ['autograder.py', 'config.ok', 'test.py']
    with ZipFile(name, 'r') as zip:
        extracted_names = zip.namelist()

        # check if files have reserved names
        bad_names = intersection(restricted_names, extracted_names)
        if bad_names:
            raise(Exception("Zipfile cannot contain files named {bad_names}"))

        zip.extractall()

        return extracted_names


def get_case_num(case):

    # First line, get case number at the end
    first_line = case[0]
    case_phrase = "".join(re.findall("Case .*", first_line))
    case_num = case_phrase.split()[-1]
    return case_num


def intersection(l1, l2):
    return list(set(l1) & set(l2))


def parseToJSON(results):

    results = results.split('---------------------------------------------------------------------\n')
    cases = results[1:-1]
    parsed_cases = parse_cases(cases)
    summary = results[-1]
    num_pass, num_fail = parse_summary(summary)

    data = {
        "cases": parsed_cases,
        "results": {
                "num_pass": num_pass,
                "num_fail": num_fail
        }
    }

    return json.dumps(data)

def parse_cases(cases):

    parsed_cases = {}
    for case in cases:
        # tokenize case into lines
        case = case.split('\n')
        case_num = get_case_num(case)
        fail_case, fail_start = parse_fail(case)
        pass_cases = [line for line in case[2:fail_start]][:-3]

        parsed_cases[case_num] = { "fail_case": fail_case, "pass_cases": pass_cases }

    return parsed_cases

def parse_fail(case):

    try: # at least one test failed
        error_start = case.index("# Error: expected")
    except: # all tests passed
        return {}, None

    # get lines detailing expected-actual fail
    error_lines = [line for line in case[error_start:] if line.startswith('#')]

    try:
        divide = error_lines.index('# but got') # divides expected and actual
        expected = "".join(error_lines[1:divide])
        actual = "".join(error_lines[divide + 1:])

        # remove leading comment
        expected = expected[1:].strip()
        actual = actual[1:].strip()
    except:
        raise(Exception("Could not divide expected and actual lines!"))

    # minus 1 since there's one newline before error_start
    return { "expected": expected, "actual": actual }, error_start - 1
    
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
