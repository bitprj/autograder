from flask_praetorian import Praetorian
from grading.autograder import grade
from flask import Flask, jsonify, render_template, request
import json
import requests
import os
from utils import *
from zipfile import ZipFile
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies
)
import config
from functools import wraps

app = Flask(__name__)

app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_ACCESS_COOKIE_PATH"] = "/"
app.config["JWT_COOKIE_CSRF_PROTECT"] = True
app.config['JWT_COOKIE_SECURE'] = False
app.config["JWT_SECRET_KEY"] = config.SECRET_KEY

jwt = JWTManager(app)
guard.init_app(app, User)


# Decorator to check if the user is logged in
def user_exists(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        form_data = request.get_json()
        errors = user_login_schema.validate(form_data)
        # If form data is not validated by the user_form_schema, then return a 500 error
        # else proceed to check if the user exists
        if errors:
            return {
                       "message": "Missing or sending incorrect login data. Double check the JSON data that it has everything needed to login."
                   }, 500
        else:
            username = form_data["username"]
            password = form_data["password"]
            user = guard.authenticate(username, password)
            if user:
                return f(*args, **kwargs)
            else:
                return {
                           "message": "User does not exist"
                       }, 404
    return wrap


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


@app.route("/login", methods=["POST"])
def login():
    form_data = request.get_json()
    username = form_data["username"]
    user = User.query.filter_by(username=username).first()
    # Create the tokens we will be sending back to the user
    resp = jsonify({"username": username
                    })
    set_access_cookies(resp, access_token)

    return resp


@app.route("/uploader", methods=['POST'])
@jwt_required
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


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    # username is the email
    username = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, unique=True, nullable=False)
    # Roles are Admin, Teacher, or Student
    roles = db.Column(db.Text, nullable=False)
    location = db.Column(db.Text, nullable=False)
    image = db.Column(db.Text, nullable=True)

    @property
    def rolenames(self):
        try:
            return self.roles.split(',')
        except Exception:
            return []
    @classmethod
    def lookup(cls, username):
        return cls.query.filter_by(username=username).one_or_none()
    @classmethod
    def identify(cls, id):
        return cls.query.get(id)
    @property
    def identity(self):
        return self.id
    def __repr__(self):
        return f"User('{self.username}')"

# https://db568d2b.ngrok.io/checkpoints/14/submit PUT
# https://db568d2b.ngrok.io/checkpoints/<int: id>/submit PUT
if __name__ == '__main__':
    app.run(debug=True)
