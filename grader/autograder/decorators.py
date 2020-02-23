from flask import request
from flask_jwt_extended import get_jwt_identity
from functools import wraps
from grader import bcrypt, guard
from grader.autograder.schemas import user_login_schema
from grader.autograder.utils import get_activity_prog, get_checkpoint_prog
from grader.models import Activity, Checkpoint, User


# Decorator to check if a activity exists
def activity_exists(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        activity = Activity.query.get(request.form["activity_id"])

        if activity:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Activity does not exist"
                   }, 404

    return wrap


# Decorator to check if a checkpoint_prog exists
def activity_prog_exists(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        data = request.form
        username = data["username"]

        # 0 index is checkpoint progress 1 index is activity progress
        activity_prog = get_activity_prog(data["activity_id"], username)

        if activity_prog:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "ActivityProgress does not exist"
                   }, 404

    return wrap


# Decorator to check if a checkpoint exists
def checkpoint_exists(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        checkpoint = Checkpoint.query.get(request.form["checkpoint_id"])
        if checkpoint:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Checkpoint does not exist"
                   }, 404

    return wrap


# Decorator to check if a checkpoint_prog exists
def checkpoint_prog_exists(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        username = get_jwt_identity()

        if not username:
            data = request.form
            username = data["username"]

        checkpoint_prog = get_checkpoint_prog(request.form["activity_id"], request.form["checkpoint_id"], username)

        if checkpoint_prog:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "CheckpointProgress does not exist"
                   }, 404

    return wrap


# Decorator to check if a cli user exists
def cli_user_exists(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        form_data = request.form
        username = form_data["username"]
        token = form_data["token"]
        user = User.query.filter_by(username=username).first()
        is_user = bcrypt.check_password_hash(user.token, token)

        if is_user:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "CLI User does not exist"
                   }, 404

    return wrap


# Decorator to check if a checkpoint is an autograder checkpoint
def is_autograder(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        checkpoint = Checkpoint.query.get(request.form["checkpoint_id"])
        if checkpoint.checkpoint_type == "Autograder":
            return f(*args, **kwargs)
        else:
            return {
                       "message": "Checkpoint is not an Autograder checkpoint"
                   }, 404

    return wrap


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
