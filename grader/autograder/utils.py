from grader import db, bcrypt
from grader.models import ActivityProgress, CheckpointProgress, Student, User
import secrets


# Function to create a token for the cli
def create_token(username):
    user = User.query.filter_by(username=username).first()
    token = None

    if not user.token:
        token = secrets.token_urlsafe(20)
        hashed_token = bcrypt.generate_password_hash(token).decode('utf8')
        user.token = hashed_token
        db.session.commit()

    return token


# Function to return activity progress objects
def get_activity_prog(activity_id, username):
    student = Student.query.filter_by(username=username).first()
    activity_prog = ActivityProgress.query.filter_by(activity_id=activity_id,
                                                     student_id=student.id).first()
    return activity_prog


# Function to return checkpoint progress objects
def get_checkpoint_prog(activity_id, checkpoint_id, username):
    student = Student.query.filter_by(username=username).first()
    activity_prog = ActivityProgress.query.filter_by(activity_id=activity_id,
                                                     student_id=student.id).first()
    checkpoint_prog = CheckpointProgress.query.filter_by(activity_progress_id=activity_prog.id,
                                                         checkpoint_id=checkpoint_id).first()

    return checkpoint_prog, activity_prog
