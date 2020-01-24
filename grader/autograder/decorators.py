from grader.autograder.schemas import user_login_schema
from flask import request
from functools import wraps
from grader import guard


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
