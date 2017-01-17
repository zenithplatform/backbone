__author__ = 'civa'

import time, json
from infrastructure.pipes import LoopingPipe

class Receiver(LoopingPipe):
    def open(self):
        self.log.info("[RECEIVER] Started")
        while True:
            self.log.info("[RECEIVER] Waiting for message")
            message = self.get_channel('receive_channel').recv_json()
            self.log.info("[RECEIVER] Message %s, type %s" % (message, type(message)))
            self.get_channel('agent_channel').send(json.dumps(message))
            time.sleep(0.1)
