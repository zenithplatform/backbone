__author__ = 'civa'

'''
Class based hooks
'''

# def main():
#     SimpleClass().init()

class TestHook(object):
    def __init__ (self, hook_function):
        self.hook = hook_function

    def __call__(self, func):
        def newf(*args, **kwargs):
            instance = args[0]
            message = args[1]
            modified_message = self.hook(message)

            new_args = []
            new_args.append(instance)
            new_args.append(modified_message)

            func(*new_args, **kwargs)

        newf.__doc__ = func.__doc__

        return newf

def message_hook(message):
    return 'Modified message'

class SomeClass(object):
    def init(self):
        self.simple_method('Init')

    @TestHook(hook_function=message_hook)
    def simple_method(self, message):
        print message

'''
'''

'''
Method based hooks
'''

def hook(func):
    def hook_and_call(*args, **kwargs):
        instance = args[0]
        msg = args[1]

        new_args = []
        new_args.append(instance)
        new_args.append('Modified message')

        return func(*new_args, **kwargs)
    return hook_and_call

class SimpleClass(object):
    @hook
    def simple_method(self, message):
        print message


'''
'''

def main():
    h = SimpleClass()
    h.simple_method('Test')

if __name__ == "__main__":
    main()
