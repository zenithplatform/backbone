__author__ = 'civa'

from local.infrastructure.pipes import Pipe

IN_REQUEST = 'distributor_input_channel'
OUT_PRODUCE = 'distributor_produce_channel'
IN_CALLBACK = 'distributor_callback_channel'
OUT_DISPATCH = 'distributor_emit_channel'

class Distributor(Pipe):
    def on_receive(self, message, context):
        name = context.channel.name

        if name == IN_REQUEST:
            self.send(OUT_PRODUCE, message)
        elif name == IN_CALLBACK:
            self.send(OUT_DISPATCH, message)