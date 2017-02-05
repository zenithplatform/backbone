__author__ = 'civa'

import sys, os, json, copy
from commons.utils import ErrorUtils
from local.infrastructure.pipes import Pipe
from local.infrastructure.messages import PipeMessage
from local.dynamic.loader import ModuleLoader
from local.processors.dummy import DummyProcessor
from local.processors.fits import FITSProcessor
#FOR TESTING PURPOSES ONLY!!!!!!!!
import random

IN = 'executor_in_channel'
OUT = 'executor_out_channel'
DEFAULT_RESULT = {'result': 'unavailable'}

class Executor(Pipe):
    def on_receive(self, message, context):
        result = DEFAULT_RESULT
        is_error = False
        errors = ''
        msg_obj = PipeMessage(message)

        #FOR TESTING PURPOSES ONLY
        #flag = bool(random.getrandbits(1))

        try:
            # if flag:
            #     raise KeyError('test')

            result = self._exec_processor(msg_obj)
        except Exception:
            is_error = True
            errors = ErrorUtils.compact_error(encode=True, compress=False)
        finally:
            if is_error:
                msg_obj.append_error(error_info=errors)
            else:
                msg_obj.append(result)

            self.send(OUT, msg_obj.reprJSON())

    def _exec_processor(self, msg_obj):
        output_location = self.config.find('configuration/processing/output')

        proc_input = self._get_exec_input(msg_obj)
        proc_input['output'] = output_location
        proc_input['request_id'] = msg_obj.meta['request_id']

        processor = self._activate_processor(msg_obj)
        config_routine = getattr(processor, 'configure')
        process_routine = getattr(processor, 'process')

        if config_routine:
            config_routine()

        if process_routine:
            return process_routine(proc_input)

    def _get_exec_input(self, msg_obj):
        return copy.deepcopy(msg_obj.body)

    def _get_exec_info(self, msg_obj):
        exec_info = msg_obj.meta['execution_info']
        return exec_info['processor'].split('.')

    def _activate_processor(self, msg_obj):
        mod, cls = self._get_exec_info(msg_obj)
        processor_location = self.config.find('configuration/processing/processors')
        activation = {'execution_dir': processor_location}
        self.ldr = ModuleLoader(processor_location)

        #load base processor module
        self.ldr.find('base')

        proc_module, proc_class = self.ldr.find(mod, cls)

        if proc_module and proc_class:
            return proc_class(**activation)

        return None
