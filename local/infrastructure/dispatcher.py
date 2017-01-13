__author__ = 'civa'

from infrastructure.pipes import Pipe, chtype, chkind

#publishes everything to the remote process (C# app)
class Dispatcher(Pipe):
    def setup(self):
        self.create_channel('dispatch_channel', 18800, chtype.inbound, chkind.publish)

    def execute(self, payload):
        self.log.info("[DISPATCHER] Sending results to another process")
        self.get_channel('dispatch_channel').send(payload)

