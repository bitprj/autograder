from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_praetorian import Praetorian
from flask_sqlalchemy import SQLAlchemy
from grader.config import *

app = Flask(__name__)

app.config["SECRET_KEY"] = SECRET_KEY
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = False
app.config["JWT_ACCESS_LIFESPAN"] = {"minutes": 45}
app.config["JWT_REFRESH_LIFESPAN"] = {"days": 1}
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_SIZE"] = 70000
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_ACCESS_COOKIE_PATH"] = "/"
app.config["JWT_COOKIE_CSRF_PROTECT"] = True
app.config['JWT_COOKIE_SECURE'] = False
app.config["JWT_SECRET_KEY"] = SECRET_KEY
app.config["CORS_HEADERS"] = "Content-Type"

bcrypt = Bcrypt()
db = SQLAlchemy(app)
jwt = JWTManager(app)
guard = Praetorian()
ma = Marshmallow()
CORS(app, supports_credentials=True, resources={r"/*": {"origins": ["*"]}})

from grader.models import User

guard.init_app(app, User)

from grader.autograder.routes import grading_bp

app.register_blueprint(grading_bp)
