__author__ = 'civa'

import json
from local.dynamic.loader import ModuleLoader
from local.dynamic import loader
from local.processors.fits import FITSProcessor
import imp

def main():
    input = {
        'uri': 'D:\\Programming\\Astronomy\\Dev\\SampleFiles\\gll_iem_v02_P6_V11_DIFFUSE.fit',
        'output': 'D:\\Programming\\Astronomy\\Dev\\ZenithPlatformSandbox\\images\\image.png',
        'req_id': 'asdasd',
        'method': 'Image'
    }

    # loader = ModuleLoader('D:\\Programming\\Astronomy\\Dev\\ZenithPlatformSandbox\\processors')
    # module, cls = loader.find('fits', 'FITSProcessor')
    # instance = cls()
    #instance = cls(**input)

    instance = FITSProcessor()
    result = instance.process(json.dumps(input))
    #result = instance.process(json.dumps(input))

    print result
    # ldr = loader.Loader()
    # ldr.load('json')
    # module_list = ['sys', 'os', 're', 'unittest', 'kjhkjh']
    # ldr.load_multiple(module_list)
    # print ldr.modules
    # ldr.enum_all()
    #

if __name__ == "__main__":
    main()
