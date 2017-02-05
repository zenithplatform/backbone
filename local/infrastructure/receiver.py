__author__ = 'civa'

import time, json
from local.infrastructure.pipes import Pipe, messagehook
from local.infrastructure.messages import PipeMessage

IN = 'receiver_in_channel'
OUT = 'receiver_out_channel'

class Receiver(Pipe):
    def preprocess(self, message, context):
        msg_obj = PipeMessage(message)

        self.log.info('[receiver] received request : {0}'.format(msg_obj.meta['request_id']))

        if not msg_obj.valid:
            msg_obj.append_error('Message is invalid')
            context.should_exit = True

        return msg_obj.reprJSON(), context

    @messagehook(hook=preprocess)
    def on_receive(self, message, context):
        if context.should_exit:
            self.exit(message)
        else:
            self.send(OUT, message)