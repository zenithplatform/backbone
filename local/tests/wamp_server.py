__author__ = 'civa'

import random
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
            # print("publish: com.myapp.heartbeat")
            # self.publish(u'com.myapp.heartbeat')

            #obj = {'counter': counter, 'foo': [1, 2, 3]}
            num = random.randint(0, 100)
            print("publish: com.myapp.topic1", num)
            self.publish(u'com.myapp.topic1', num)

            #Handle transport lost exc on publish, when router is unavaliable
            '''
            2017-02-21T07:26:55+0100 While firing onJoin: Traceback (most recent call last):
              File "C:\Python27\lib\site-packages\twisted\internet\defer.py", line 459, in callback
                self._startRunCallbacks(result)
              File "C:\Python27\lib\site-packages\twisted\internet\defer.py", line 567, in _startRunCallbacks
                self._runCallbacks()
              File "C:\Python27\lib\site-packages\twisted\internet\defer.py", line 653, in _runCallbacks
                current.result = callback(current.result, *args, **kw)
              File "C:\Python27\lib\site-packages\twisted\internet\defer.py", line 1357, in gotResult
                _inlineCallbacks(r, g, deferred)
            --- <exception caught here> ---
              File "C:\Python27\lib\site-packages\twisted\internet\defer.py", line 1301, in _inlineCallbacks
                result = g.send(result)
              File "D:/Programming/Astronomy/Dev/ZenithPlatform/backbone/local/tests/wamp_server.py", line 27, in onJoin
                self.publish(u'com.myapp.topic1', num)
              File "C:\Python27\lib\site-packages\autobahn\wamp\protocol.py", line 1138, in publish
                raise exception.TransportLost()
            autobahn.wamp.exception.TransportLost:
            '''

            # self.publish(u'com.myapp.topic1', random.randint(0, 100), 23,
            #              c="Hello", d=obj)

            counter += 1
            yield sleep(1)


if __name__ == '__main__':
    runner = ApplicationRunner(url=u"ws://127.0.0.1:9999/wsdemo", realm=u"realm1")
    # runner = ApplicationRunner(
    #     environ.get("AUTOBAHN_DEMO_ROUTER", u"ws://127.0.0.1:9999/ws"),
    #     u"realm1",
    # )
    runner.run(Component)
