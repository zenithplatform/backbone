__author__ = 'civa'

import inspect

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

def m_hook(message):
    return 'Modified message'

class SomeClass(object):
    def init(self):
        self.simple_method('Init')

    @TestHook(hook_function=m_hook)
    def simple_method(self, message):
        print message

'''
'''

'''
Method based hooks
'''

#  def hook(func):
#     def hook_and_call(*args, **kwargs):
#         instance = args[0]
#         msg = args[1]
#
#         new_args = []
#         new_args.append(instance)
#         new_args.append('Modified message')
#
#         return func(*new_args, **kwargs)
#     return hook_and_call

# def message_hook(func):
#    def func_wrapper(message):
#        return func(message)
#    return func_wrapper

class messagehook(object):
    def __init__ (self, hook):
        self.hook = hook

    def __call__(self, func):
        def newf(*args, **kwargs):
            instance = args[0]
            message = args[1]
            modified_message = self.hook(instance, message)

            new_args = []
            new_args.append(instance)
            new_args.append(modified_message)

            func(*new_args, **kwargs)

        newf.__doc__ = func.__doc__

        return newf

class SimpleClass(object):
    def preprocess(self, message):
        print('Hooked message : {}'.format(message))
        return 'Hooked'

    @messagehook(hook=preprocess)
    def simple_method(self, message):
        print message

    def has_hook(self):
        for name in dir(self):
            class_func = getattr(type(self), name, None)
            if isinstance(class_func, messagehook):
                print 'Found hook : {0}'.format(class_func)
'''
'''

def main():
    h = SimpleClass()
    h.simple_method('Test')

if __name__ == "__main__":
    main()
