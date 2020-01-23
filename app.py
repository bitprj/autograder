from grading.autograder import grade
from flask import Flask, jsonify, render_template, request
import json
import requests
import os
from utils import *
from zipfile import ZipFile

app = Flask(__name__)

posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


@app.route("/")
@app.route("/home")
def home():
    response = jsonify({"message":'hello it went through'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response  # print a raw representation

@app.route("/test", methods=['GET', 'POST', 'OPTIONS'])
def test():
    if (request.method == 'POST'):
        f = request.files['src']
        f2 = request.files['tests']

        save_file(f)
        save_file(f2)

    response = jsonify({"message":'hello it went through'})
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    response.headers.add('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'X-PINGOTHER, Content-Type')
    response.headers.add('Access-Control-Allow-Credentials', 'true')

    return response  # print a raw representation

@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/upload", methods=['GET', 'POST'])
def upload():
    return render_template('upload.html', title='Upload', endpoint='/uploader')


@app.route("/uploader", methods=['POST'])
def upload_file():

    try:
        os.chdir("./grading")
        src_file = request.files["src"]
        tests_file = request.files["tests"]
        src_filename = save_file(src_file)
        tests_filename = save_file(tests_file)

        filenames = extract(src_filename) + extract(tests_filename)
        src_names = [name for name in filenames if name.endswith('.py')]
        test_names = [name for name in filenames if name.endswith('.test')]
        src_files, test_files = get_files(src_names, test_names)

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
        # headers = {
        #     'Access-Control-Allow-Origin': '*',
        #     'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
        #     'Access-Control-Allow-Headers': 'X-PINGOTHER, Content-Type'
        #     # 'Content-Type': 'application/json',
        #     # 'Access-Control-Allow-Origin': '*'
        # }
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        response.headers.add('Content-Type', 'application/json')
        response.headers.add('Access-Control-Allow-Headers', 'X-PINGOTHER, Content-Type')
        response.headers.add('Access-Control-Allow-Credentials', 'true')

        # response = requests.put(
        #     url=url, data=json.dumps(data),
        #     headers=headers
        # )
        #response = requests.put(
        #    url=url, data=json.dumps(data),
        #    headers={
        #        'Content-Type': 'application/json',
        #        'Access-Control-Allow-Origin': '*'
        #    }
        #)
        # response.headers.add(headers)
        # Remove generated files
        for name in filenames:
            os.remove(name)
    except Exception as e:
        os.chdir("..")
        print(e)
        return "<h1>Error!</h1>"

    os.chdir("..")
    return response  # print a raw representation


# https://db568d2b.ngrok.io/checkpoints/14/submit PUT
# https://db568d2b.ngrok.io/checkpoints/<int: id>/submit PUT
if __name__ == '__main__':
    app.run(debug=True)
