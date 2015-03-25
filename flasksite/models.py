from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()
#model for user login and roles
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(100))
    email = db.Column(db.String(100))
    role = db.Column(db.String(100))

    def __init__(self, nickname, email, role):

        self.nickname = nickname.lower()
        self.email = email.lower()
        self.role = role
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return '<User %r>' % (self.nickname)