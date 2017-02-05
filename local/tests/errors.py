__author__ = 'civa'

import sys, json, traceback, base64
from local.infrastructure.pipes import PipeError

def main():
    dict = {}
    error_info = ''

    try:
        err = PipeError()
        ghost = dict['test']
    except KeyError:
         error_info = traceback.format_exc()
    except ValueError:
        error_info = traceback.format_exc()
        #exc_type, exc_value, exc_traceback = sys.exc_info()
    except Exception:
        error_info = traceback.format_exc()
        #exc_type, exc_value, exc_traceback = sys.exc_info()
    finally:
        print error_info
        pass

    print base64.b64encode(error_info)

if __name__ == "__main__":
    main()
