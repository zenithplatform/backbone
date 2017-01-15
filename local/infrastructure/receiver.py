__author__ = 'civa'

import time, json
from infrastructure.pipes import LoopingPipe, chtype, chkind

class Receiver(LoopingPipe):
    def setup(self):
        self.create_channel('receiver_channel', 18801, chtype.inbound, chkind.pull)
        self.create_channel('agent_channel', 18802, chtype.outbound, chkind.push)

    def execute(self):
        self.log.info("[RECEIVER] Started")
        while True:
            self.log.info("[RECEIVER] Waiting for message")
            message = self.get_channel('receiver_channel').recv_json()
            self.log.info("[RECEIVER] Message %s, type %s" % (message, type(message)))
            self.get_channel('agent_channel').send(json.dumps(message))
            time.sleep(0.1)
