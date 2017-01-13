__author__ = 'civa'
#from core.storage import db_manager
#from auth_hub.storage.dbaccess_OBSOLETE import DataProvider, DbAccessException
from hubs.auth.model.app_user import AppUser

def data_test():
    user = AppUser()
    result = user.create_new('testemail@mail.com', 'civa', 'test')


    #user = AppUser()
    #result = user.create_new('testemail@mail.com', 'civa', 'test')

    #result = user.login('civa', 'test')

    test = ''
    #provider = DataProvider()


        #provider.create('Zenith', 'postgres', 'disaster')
       # data = (1, "civa", "test_pass", "", False)
        #result = provider.execute_query('INSERT INTO "Users" (username, password, access_token, logged_in) VALUES (%s, %s, %s, %s, %s);', data)


    #result = provider.execute_query('SELECT * FROM users;', None)
    #data = (1, "civa", "test_pass", "", False)
    #result = provider.execute_query('INSERT INTO "Users" (user_id, username, password, access_token, logged_in) VALUES (%s, %s, %s, %s, %s);', data)

    #data = ('civa', 'test_pass')
    #result = provider.execute_proc('login_user', data)
    #provider.dispose()

    #print result

if __name__ == "__main__":
    data_test()

