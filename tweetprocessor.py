u'''
Created on 19 jul. 2013

@author: patveck
'''

import SseHTTPServer
import Queue
import threading
import SocketServer
import time
import random
import actions
import buildinfo


def process_tweets(infile, port):
    u"""Main entry point for the server-side component of the Twitter dashboard.
    It has two responsibilities:
    1. Provide an event queue factory to SseHTTPServer.SseHTTPRequestHandler. SseHTTPRequestHandler is the
       piece of Python code that responses to requests sent by the (JavaScript) client running in a browser.
       This piece of code needs to get the contents of its responses from somewhere; to get those responses, it
       calls the factory that we provide here;
    2. Start two components in parallel:
       a. The ECA rule engine that takes tweets from some source, processes them, and based on that puts messages
          in a queue;
       b. A server that listens to a certain port and starts a SseHTTPRequestHandler for every incomming
          connection
    """

    # Responsibility 1: provide factory:
    SseHTTPServer.SseHTTPRequestHandler.event_queue_factory = subscribe

    for message in MYQUEUE:
        for count in LISTENERS:
            LISTENERS[count].put(message)

    # Responsibility 2a: start ECA rule engine. Is currently just a test stub
    # called queueFiller:
    queue_filler = QueueFiller()
    queue_filler.start()

    # Responsibility 2b: start server
    httpd = SocketServer.ThreadingTCPServer((u"", port),
                            SseHTTPServer.SseHTTPRequestHandler)
    httpd.serve_forever()

MYQUEUE = [{u"event": u"test", u"data": [u"Line 1 of first message.",
                                      u"Line 2 of first message."]},
           {u"event": u"test", u"data": [u"Line 1 of second message.",
                                      u"Line 2 of second message."]}
          ]

BUILDINFO = buildinfo.get_buildinfo(__file__)


def subscribe(listener_id):
    u"""Event source factory for SseHTTPServer.SseHTTPRequestHandler."""
    chart_options = {u"title": {u"text": u"Browser market shares"},
                     u"series": [{u"type": u"pie",
                                 u"name": u"Browser share",
                                        u"data": [[u"Firefox", 45.0],
                                                 [u"IE", 26.8],
                                                 [u"Chrome", 12.8],
                                                 [u"Safari", 8.5],
                                                 [u"Opera", 6.2],
                                                 [u"Others", 0.7]
                                                 ]}]}

    _new_queue = Queue.Queue()
    _new_queue.put(actions.send_buildinfo(BUILDINFO))
    _new_queue.put(actions.create_alert_gadget(u"cell0", u"myAlerter"))
    _new_queue.put(actions.create_alert_gadget(u"cell4", u"serverinfo"))
    _new_queue.put(actions.alert(u"Server started!", u"serverinfo"))
    _new_queue.put(actions.create_general_chart(u"chart1", chart_options))
    LISTENERS[listener_id] = _new_queue
    if not EVENT.is_set():
        EVENT.set()
    return _new_queue

LISTENERS = {}

EVENT = threading.Event()


class QueueFiller(threading.Thread):

    u"""Thread class that fills queue with heartbeat messages (one per second)

    Module 1.1 in the INF program doesn't teach classes, so we try to avoid
    them. Maybe the standard library allows to just run a function in a thread.
    """

    def _send_to_all_listeners(self, message):
        for count in LISTENERS:
            LISTENERS[count].put(message)

    def run(self):
        EVENT.wait()
        print u"queueuFiller: started in thread %s." % self.ident
        self._send_to_all_listeners(actions.message(u"queueuFiller: started in "
                                                    u"server thread %s." %
                                                    self.ident))
        alert_counter = 0
        while True:
            self._send_to_all_listeners(actions.add_point(u"mychart",
                                                    int(time.time()) * 1000,
                                                    random.random()))
            if random.random() > .9:
                alert_counter += 1
                self._send_to_all_listeners(actions.alert(u"Random alert %s!" %
                                                          alert_counter,
                                                          u"myAlerter"))
            time.sleep(1)


if __name__ == u'__main__':
    pass
