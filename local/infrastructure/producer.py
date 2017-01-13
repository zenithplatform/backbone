__author__ = 'civa'

from infrastructure.pipes import Pipe, chtype, chkind

class Producer(Pipe):
    def setup(self):
        self.create_channel('result_channel', 18803, chtype.outbound, chkind.push)

    def execute(self, *args, **kwargs):
        args = list(args)
        obj = args[0]
        self.log.info("[PRODUCER] : Sending results to agent")
        self.get_channel('result_channel').send_json(obj=obj, **kwargs)
