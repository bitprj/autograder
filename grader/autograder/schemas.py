from grader import ma
from marshmallow import fields


# This schema is used to validate user login information
class UserLoginSchema(ma.Schema):
    username = fields.Email(required=True)
    password = fields.Str(required=True)


user_login_schema = UserLoginSchema()
