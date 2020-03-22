from grader import ma
from marshmallow import fields


# This schema is used to display submission data
class SubmissionSchema(ma.Schema):
    results = fields.Dict(required=True)
    date_time = fields.DateTime(required=True)

    class Meta:
        # Fields to show when sending data
        fields = ("results", "date_time")
        ordered = True


# This schema is used to validate user login information
class UserLoginSchema(ma.Schema):
    username = fields.Email(required=True)
    password = fields.Str(required=True)


submission_schema = SubmissionSchema()
user_login_schema = UserLoginSchema()
