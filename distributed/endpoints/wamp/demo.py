__author__ = 'civa'

import random
from os import environ

from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.util import sleep
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner


class Component(ApplicationSession):
    """
    An application component that publishes events with no payload
    and with complex payload every second.
    """

    @inlineCallbacks
    def onJoin(self, details):
        print("session attached")

        counter = 0
        while True:
            print("publish: com.myapp.heartbeat")
            self.publish(u'com.myapp.heartbeat')

            obj = {'counter': counter, 'foo': [1, 2, 3]}
            print("publish: com.myapp.topic2", obj)
            self.publish(u'com.myapp.topic2', random.randint(0, 100), 23,
                         c="Hello", d=obj)

            counter += 1
            yield sleep(1)


if __name__ == '__main__':
    runner = ApplicationRunner(
        environ.get("AUTOBAHN_DEMO_ROUTER", u"ws://127.0.0.1:8080/ws"),
        u"crossbardemo",
    )
    runner.run(Component)
