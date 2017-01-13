__author__ = 'civa'

from jsonweb.encode import to_object

from hubs.auth.storage.dbaccess_OBSOLETE import DataProvider, DbAccessException
from hubs.auth.model.enum import UserStatus

def appuser_encoder(appuser):
    return {"user_id":              appuser.user_id,
            "username":             appuser.username,
            "email_address":        appuser.email_address,
            "status":               appuser.status,
            "access_token":         appuser.access_token,
            "logged_in":            appuser.logged_in,
            "valid":                appuser.isValid}

@to_object(handler=appuser_encoder)
class AppUser(object):

    user_id = 0
    username = ''
    password = ''
    email_address = ''
    access_token = ''
    status = UserStatus.Unknown
    isValid = False
    logged_in = False

    def login(self, username, password):
        self.username = username
        self.password = password

        try:
            provider = DataProvider()
            provider.create('Zenith', 'postgres', 'disaster')
        except DbAccessException as e:
            status = UserStatus.Unknown
            self.isValid = False
            print e

        data = (self.username, self.password)

        try:
            result = provider.execute_proc('authenticate_user', data)

            self.user_id = result[0]

            if self.user_id > 0:
                self.access_token = create_user_token(self.user_id)
                data = (self.user_id, self.access_token)

                result = provider.execute_proc('assign_user_token', data)

                if result:
                    self.email_address = result[1]
                    self.username = result[2]

                    self.isValid = True
                    self.status = UserStatus.Valid
                else:
                    status = UserStatus.Unknown
                    self.isValid = False

                    return
            else:
                status = UserStatus.InvalidCredentials
                self.isValid = False

                return

        except DbAccessException as e:
            self.status = UserStatus.Unknown
            self.isValid = False
            print e
        finally:
            provider.dispose()

    def create_new(self, emailAddress, username, password):
        self.email_address = emailAddress
        self.username = username
        self.password = password

        try:
            provider = DataProvider()
            provider.create('Zenith', 'postgres', 'disaster')

            data = (self.email_address, self.username, self.password, self.access_token, self.logged_in)
            result = provider.execute_query('INSERT INTO users (email_address, username, password, access_token, logged_in) VALUES (%s, %s, %s, %s, %s);', data)

        except DbAccessException as e:
            self.isValid = False

            if e.status == 1:
                self.status = UserStatus.AlreadyExists
            else:
                self.status = UserStatus.Unknown

            print e
        finally:
            provider.dispose()

