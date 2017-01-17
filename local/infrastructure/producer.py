__author__ = 'civa'

from infrastructure.pipes import Pipe

class Producer(Pipe):
    def send(self, *args, **kwargs):
        args = list(args)
        obj = args[0]
        self.log.info("[PRODUCER] : Sending results to agent")
        self.get_channel('result_channel').send_json(obj=obj, **kwargs)
