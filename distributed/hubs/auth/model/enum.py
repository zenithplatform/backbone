__author__ = 'civa'

class DataAccessStatus:
    Success, AlreadyExists, DoesNotExist, UnknownError, ServerUnavailable, InvalidCredentials = range(6)

class UserStatus:
    Valid, AlreadyExists, DoesNotExist, Unknown, InvalidCredentials = range(5)
