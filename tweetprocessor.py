'''
Created on 19 jul. 2013

@author: patveck
'''

import SseHTTPServer
import queue
import threading
import socketserver
import time
import random
import actions


def process_tweets(infile, port):
    """Main entry point for the server-side component of the Twitter dashboard.
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
    httpd = socketserver.ThreadingTCPServer(("", port),
                            SseHTTPServer.SseHTTPRequestHandler)
    httpd.serve_forever()

MYQUEUE = [{"event": "test", "data": ["Line 1 of first message.",
                                      "Line 2 of first message."]},
           {"event": "test", "data": ["Line 1 of second message.",
                                      "Line 2 of second message."]}
          ]


def subscribe(listener_id):
    """Event source factory for SseHTTPServer.SseHTTPRequestHandler."""
    _new_queue = queue.Queue()
    LISTENERS[listener_id] = _new_queue
    return _new_queue

LISTENERS = {}


class QueueFiller(threading.Thread):

    """Thread class that fills queue with heartbeat messages (one per second)

    Module 1.1 in the INF program doesn't teach classes, so we try to avoid
    them. Maybe the standard library allows to just run a function in a thread.
    """

    chart_options = {"title": {"text": "Browser market shares"},
                     "series": [{"type": "pie",
                                 "name": "Browser share",
                                        "data": [["Firefox", 45.0],
                                                 ["IE", 26.8],
                                                 ["Chrome", 12.8],
                                                 ["Safari", 8.5],
                                                 ["Opera", 6.2],
                                                 ["Others", 0.7]
                                                 ]}]}

    def _send_to_all_listeners(self, message):
        for count in LISTENERS:
            LISTENERS[count].put(message)

    def run(self):
        print("queueuFiller: started in thread %s." % self.ident)
        self._send_to_all_listeners(actions.message("queueuFiller: started in "
                                                    "server thread %s." %
                                                    self.ident))
        self._send_to_all_listeners(actions.create_general_chart("chart1",
                                                        self.chart_options))
        while True:
            self._send_to_all_listeners(actions.add_point("mychart",
                                                    int(time.time()) * 1000,
                                                    random.random()))
            time.sleep(1)


if __name__ == '__main__':
    pass
