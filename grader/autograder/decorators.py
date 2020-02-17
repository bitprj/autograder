from flask import request
from flask_jwt_extended import get_jwt_identity
from functools import wraps
from grader import guard
from grader.autograder.schemas import user_login_schema
from grader.models import Activity, ActivityProgress, CheckpointProgress, Student


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


# Decorator to check if a checkpoint exists
def checkpoint_exists(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        checkpoint = Activity.query.get(request.form["checkpoint_id"])

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
        student = Student.query.filter_by(username=username).first()
        activity_prog = ActivityProgress.query.filter_by(activity_id=request.form["activity_id"],
                                                         student_id=student.id).first()
        checkpoint_prog = CheckpointProgress.query.filter_by(activity_progress_id=activity_prog.id,
                                                             checkpoint_id=request.form["checkpoint_id"]).first()
        if checkpoint_prog:
            return f(*args, **kwargs)
        else:
            return {
                       "message": "CheckpointProgress does not exist"
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
