from adjustable_invoice.svc.base import session_scope
from adjustable_invoice.svc.users import exceptions
from adjustable_invoice.svc.users.models import User


class UsersAPI():

    def create_user(email, password):
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
            return new_user
