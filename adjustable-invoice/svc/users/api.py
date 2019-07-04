from .svc.base import session_scope
from .svc.users import exceptions
from .svc.users.models import User


class UsersAPI():

    def create_user(self, email, password):
        with session_scope() as session:
            existing_user = (
                session.query(User)
                .filter_by(email=email)
                .first()
            )
            if existing_user:
                raise exceptions.UserAlreadyExists(
                    'A user already exists with that email')

            new_user = User()
            new_user.email = email
            new_user.password = password
            session.add(new_user)
