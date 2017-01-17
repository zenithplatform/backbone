__author__ = 'civa'

from infrastructure.pipes import Pipe

#publishes everything to the remote process
class Dispatcher(Pipe):
    def send(self, *args, **kwargs):
        args = list(args)
        payload = args[0]
        self.log.info("[DISPATCHER] Sending %s to another process"%(payload))
        self.get_channel('dispatch_channel').send(payload)
        self.log.info("[DISPATCHER] Message sent")

