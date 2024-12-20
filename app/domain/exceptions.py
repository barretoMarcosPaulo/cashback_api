class UserEmailAlreadyExistsError(Exception):
    pass


class UserCPFAlreadyExistsError(Exception):
    pass


class UserNotFoundError(Exception):
    pass


class AuthenticationError(Exception):
    pass
