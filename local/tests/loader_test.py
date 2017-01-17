__author__ = 'civa'

from dynamic import loader

def main():
    ldr = loader.Loader()
    ldr.load('json')
    module_list = ['sys', 'os', 're', 'unittest', 'kjhkjh']
    ldr.load_multiple(module_list)
    print ldr.modules
    ldr.enum_all()
    #

if __name__ == "__main__":
    main()
