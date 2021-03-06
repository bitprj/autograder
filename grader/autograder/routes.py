from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, set_access_cookies
from grader import app
from grader.models import Student
from grader.autograder.decorators import activity_exists, activity_prog_exists, checkpoint_exists, \
    checkpoint_prog_exists, cli_user_exists, is_autograder, user_exists
from grader.autograder.schemas import submission_schema
from grader.utils.fetch_utils import get_checkpoint_prog, get_src_test_names, get_src_test_names_cli
from grader.utils.create_utils import create_pusher_activity, create_submission, create_token
from grader.utils.file_utils import *
from grading.autograder import grade
import os

grading_bp = Blueprint("grading", __name__)


@app.route("/test", methods=['GET', 'POST', 'OPTIONS'])
def test():
    if request.method == 'POST':
        f = request.files['src']
        f2 = request.files['tests']

        save_file(f)
        save_file(f2)

    return "ok"  # print a raw representation


@app.route("/login", methods=["POST"])
@user_exists
def login():
    form_data = request.get_json()
    username = form_data["username"]
    token = create_token(username)
    # Create the tokens we will be sending back to the user
    access_token = create_access_token(identity=username)
    resp = jsonify({"username": username,
                    "token": token
                    })
    set_access_cookies(resp, access_token)

    return resp


@app.route("/uploader", methods=['POST'])
# @jwt_required
@activity_exists
@checkpoint_exists
@checkpoint_prog_exists
def upload_file():
    data = request.form
    student = Student.query.filter_by(email=data["email"]).first()
    checkpoint_prog = get_checkpoint_prog(data["activity_id"], data["checkpoint_id"], student.username)

    if "grading" in os.getcwd():
        os.chdir("..")
    os.chdir("./grading")

    # index 0 returns src_names and index 1 returns tests_names
    filenames = get_src_test_names(checkpoint_prog, request.files)
    # Runs okPy Autograder
    results = grade(filenames[0], filenames[1])
    test_results = parseToJSON(results, filenames[3])
    submission = create_submission(test_results, checkpoint_prog)
    remove_files(filenames[0] + filenames[1] + filenames[2])

    return submission_schema.dump(submission)


@app.route("/uploader/cli", methods=['POST'])
@checkpoint_exists
@is_autograder
@activity_exists
@cli_user_exists
@activity_prog_exists
@checkpoint_prog_exists
def upload_file_cli():
    data = request.form
    checkpoint_prog = get_checkpoint_prog(data["activity_id"], data["checkpoint_id"], data["username"])

    if "grading" in os.getcwd():
        os.chdir("..")
    os.chdir("./grading")

    # index 0 returns src_names and index 1 returns tests_names
    filenames = get_src_test_names_cli(checkpoint_prog, request.files)
    # Runs okPy Autograder
    results = grade(filenames[0], filenames[1])
    test_results = parseToJSON(results, filenames[3])
    submission = create_submission(test_results, checkpoint_prog)
    remove_files(filenames[0] + filenames[1] + filenames[2])
    create_pusher_activity(test_results, data["username"])

    return submission_schema.dump(submission)

