from grading.autograder import grade
from flask import Flask, render_template, request
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
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/upload", methods=['GET', 'POST'])
def upload():
    return render_template('upload.html', title='Upload', endpoint='/uploader')


@app.route("/uploader/", methods=['POST'])
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

        # run autograder
        results = grade(src_names, test_names)

        # parse results into JSON
        JSON_results = parseToJSON(results)
        url = "https://a335ce4b.ngrok.io"
        jwt_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1Nzg0NTMyMzEsImV4cCI6MTU3ODQ1NTkzMSwianRpIjoiZTI5MGJkYTYtYWYzOS00Y2IyLWEzOGItYWUxZGYyZmU4OWE5IiwiaWQiOjQsInJscyI6IlN0dWRlbnQiLCJyZl9leHAiOjE1Nzg1Mzk2MzF9.kgVPXB3fUP9e9zRjlnQJ7TO0MoaIuH0MVOTYZoQhX0Y"
        data = {
            "JSON_DATA": JSON_results,
            "jwt_token": jwt_token
        }

        response = requests.put(
            url=url, data=json.dumps(data),
            headers={'Content-Type': 'application/json'}
        )

        print(response)

        # Remove generated files
        for name in filenames:
            os.remove(name)
    except Exception as e:
        os.chdir("..")
        print(e)
        return "<h1>Error!</h1>"

    os.chdir("..")
    return JSON_results  # print a raw representation


# https://db568d2b.ngrok.io/checkpoints/14/submit PUT
# https://db568d2b.ngrok.io/checkpoints/<int: id>/submit PUT
if __name__ == '__main__':
    app.run(debug=True)
