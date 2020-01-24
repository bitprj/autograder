from grader import db


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