from grader import pusher_client
from grader.utils.file_utils import extract, save_file
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
    src_file = files["src"]
    src_filename = save_file(src_file)
    tests_file = checkpoint_prog.checkpoint.tests_zip
    urllib.request.urlretrieve("http://" + tests_file, "tests.zip")
    filenames = extract(src_filename) + extract("tests.zip")

    src_names = [name for name in filenames if name.endswith('.py') and not name.startswith("_")]
    test_names = [name for name in filenames if name.endswith('.test')]
    txt_names = [name for name in filenames if name.endswith('.txt')]
    test_names.sort()
    print(src_names)
    print(test_names)
    print(txt_names)
    return src_names, test_names, txt_names


# Gets ths src zip and tests zip names when students submit through a cli
def get_src_test_names_cli(checkpoint_prog, files):
    tests_file = checkpoint_prog.checkpoint.tests_zip
    urllib.request.urlretrieve("http://" + tests_file, "tests.zip")
    src_file_names = get_file_names(files)
    filenames = src_file_names + extract("tests.zip")

    src_names = [name for name in filenames if name.endswith('.py')]
    test_names = [name for name in filenames if name.endswith('.test')]

    return src_names, test_names
