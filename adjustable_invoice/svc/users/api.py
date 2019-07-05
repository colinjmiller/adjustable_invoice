import bcrypt

from adjustable_invoice.svc.base import session_scope
from adjustable_invoice.svc.users import exceptions
from adjustable_invoice.svc.users.models import AppUser, UserWrapper
from flask_login import AnonymousUserMixin


class UsersAPI():

    def user_to_dict(user):
        return {
            'id': user.id,
            'email': user.email,
            'password': user.password
        }

    def create_user(email, password):
        with session_scope() as session:
            existing_user = (
                session.query(AppUser)
                .filter_by(email=email)
                .first()
            )
            if existing_user:
                raise exceptions.UserAlreadyExists(
                    'A user already exists with that email')

            new_user = AppUser()
            new_user.email = email
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt(12))
            new_user.password = hashed_password
            session.add(new_user)
            return UsersAPI.user_to_dict(new_user)

    def authenticate_user(email, password):
        with session_scope() as session:
            user = (
                session.query(AppUser)
                .filter_by(email=email)
                .first()
            )

            if not user:
                raise exceptions.AuthenticationFailed(
                    'We did not find a user with that email')

            password_match = bcrypt.checkpw(password, user.password)

            if not password_match:
                raise exceptions.AuthenticationFailed(
                    'We did not find a user with that email ' +
                    'and password combination')

            return UsersAPI.user_to_dict(user)

    def get_user_by_id(user_id):
        with session_scope() as session:
            user = (
                session.query(AppUser)
                .filter_by(id=user_id)
                .first()
            )

            if not user:
                return None

            return UserWrapper(UsersAPI.user_to_dict(user))
