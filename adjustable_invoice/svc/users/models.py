from flask_login import UserMixin
from adjustable_invoice.svc.base import db


class AppUser(db.Model):
    __tablename__ = 'app_user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)


class UserWrapper(UserMixin):

    def __init__(self, user):
        self.id = user['id']
        self.email = user['email']

    def __repr__(self):
        return f"User id: {self.id}, email: {self.email}"
