from grader.utils.file_utils import edit_input, extract, save_file
from grader.models import ActivityProgress, CheckpointProgress, Student
import urllib.request


# Function to return activity progress objects
def get_activity_prog(activity_id, username):
    student = Student.query.filter_by(username=username).first()
    activity_prog = ActivityProgress.query.filter_by(activity_id=activity_id,
                                                     student_id=student.id).first()
    return activity_prog


# Function to return checkpoint progress objects
def get_checkpoint_prog(activity_id, checkpoint_id, username):
    student = Student.query.filter_by(username=username).first()
    activity_prog = ActivityProgress.query.filter_by(activity_id=activity_id,
                                                     student_id=student.id).first()
    checkpoint_prog = CheckpointProgress.query.filter_by(activity_progress_id=activity_prog.id,
                                                         checkpoint_id=checkpoint_id).first()

    return checkpoint_prog


# Function to get src files when student submits through a cli
def get_file_names(files):
    src_file_names = []
    restricted_names = ['autograder.py', 'config.ok', 'test.py']

    for file in files:
        if file in restricted_names:
            return {"message": "File could not contain 'autograder.py', 'config.ok', 'test.py' files"}
        files[file].save("./" + file)
        src_file_names.append(file)

    return src_file_names


def get_src_test_names(checkpoint_prog, files):
    src_file = files["content"]
    src_filename = save_file(src_file)
    urllib.request.urlretrieve(checkpoint_prog.checkpoint.tests_zip, "tests.zip")
    filenames = extract(src_filename) + extract("tests.zip")

    return separate_files(filenames)


# Gets ths src zip and tests zip names when students submit through a cli
def get_src_test_names_cli(checkpoint_prog, files):
    src_file_names = get_file_names(files)
    urllib.request.urlretrieve(checkpoint_prog.checkpoint.tests_zip, "tests.zip")
    filenames = src_file_names + extract("tests.zip")

    return separate_files(filenames)


# Function to sepereate files to .txt, .text, and .py files
def separate_files(filenames):
    src_names = [name for name in filenames if name.endswith('.py') and not name.startswith("_")]
    test_names = [name for name in filenames if name.endswith('.test') and not name.startswith("_")]
    txt_names = [name for name in filenames if name.endswith('.txt') and not name.startswith("_")]
    txt_names.sort()
    test_names.sort()
    edit_input(src_names, txt_names)
    test_case_names = get_test_names(test_names)

    return src_names, test_names, txt_names, test_case_names


# Function to get the name for each test case
def get_test_names(test_names):
    test_case_names = []

    for test in test_names:
        with open(test, 'r') as fin:
            data = fin.read().splitlines(True)
            test_case_names.append(data[0][:-1])
        with open(test, 'w') as fout:
            fout.writelines(data[1:])

    return test_case_names
