__author__ = 'civa'

import json
from shared import security

def pass_test():
    str = '{"username":"test","password":"testpass"}'

    data = json.loads(str)

    input_pass = 'disaster'
    hashed_pass = '+IOsYZLzXA9n5gbqURCGh7+2wObuZ9GuQgIyv35HtPPGLx7a'
    result = security.check_hash(input_pass, hashed_pass, False)

    if result:
        print 'Valid'
    else:
        print 'Invalid'

    #pass_hash = security.make_hash('disaster')
    #print pass_hash

if __name__ == "__main__":
    #get_vizier()
    pass_test()
