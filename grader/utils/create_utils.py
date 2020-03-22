from datetime import datetime
from grader import db, bcrypt, pusher_client
from grader.models import Submission, User
import secrets


# Function to notify a student that their activity has been graded
def create_pusher_activity(data, username):
    channel_name = username + "-autograder-cli"
    pusher_client.trigger(channel_name, 'new-record', {'data': data})

    return


# Function to create a submission and add it to the checkpoint progress
def create_submission(test_results, checkpoint_prog):
    submission = Submission(results=test_results,
                            progress_id=checkpoint_prog.id,
                            date_time=datetime.now()
                            )
    db.session.add(submission)
    db.session.commit()
    checkpoint_prog.is_completed = True
    checkpoint_prog.submissions.append(submission)
    db.session.commit()

    return submission


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
