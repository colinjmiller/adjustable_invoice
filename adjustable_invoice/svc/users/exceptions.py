class BaseUsersException(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class UserAlreadyExists(BaseUsersException):
    pass


class AuthenticationFailed(BaseUsersException):
    pass


class UserNotFound(BaseUsersException):
    pass
