from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, set_access_cookies
from grader.autograder.decorators import user_exists
from grader import app
from grader.utils import *
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

    response = jsonify({"message": 'hello it went through'})
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    response.headers.add('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'X-PINGOTHER, Content-Type')
    response.headers.add('Access-Control-Allow-Credentials', 'true')

    return response  # print a raw representation


@app.route("/login", methods=["POST"])
@user_exists
def login():
    form_data = request.get_json()
    username = form_data["username"]

    # Create the tokens we will be sending back to the user
    access_token = create_access_token(identity=username)
    resp = jsonify({"username": username
                    })
    set_access_cookies(resp, access_token)

    return resp


@app.route("/uploader", methods=['POST'])
#@jwt_required
def upload_file():
    try:
        username = get_jwt_identity()
        os.chdir("./grading")
        src_file = request.files["src"]
        tests_file = request.files["tests"]
        src_filename = save_file(src_file)
        tests_filename = save_file(tests_file)

        filenames = extract(src_filename) + extract(tests_filename)
        src_names = [name for name in filenames if name.endswith('.py')]
        test_names = [name for name in filenames if name.endswith('.test')]
        # JOHN PLEASE ADJUST THE COMMENT CODE
        # src_files, test_files = get_files(src_names, test_names)

        # run autograder
        results = grade(src_names, test_names)

        # parse results into JSON
        JSON_results = parseToJSON(results)
        url = "https://darlene-backend.herokuapp.com/checkpoints" + request.form["checkpoint_id"] + "/submit"
        jwt_token = request.form["jwt_token"]
        data = {
            "results": JSON_results,
            "jwt_token": jwt_token
        }

        response = jsonify(data)

        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        response.headers.add('Content-Type', 'application/json')
        response.headers.add('Access-Control-Allow-Headers', 'X-PINGOTHER, Content-Type')
        response.headers.add('Access-Control-Allow-Credentials', 'true')

        for name in filenames:
            os.remove(name)
    except Exception as e:
        os.chdir("..")
        print(e)
        return "<h1>Error!</h1>"

    os.chdir("..")
    return response  # print a raw representation
