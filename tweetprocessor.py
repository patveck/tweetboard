'''
Created on 19 jul. 2013

@author: patveck
'''

import SseHTTPServer
import queue
import threading
import logging
import socketserver
import time
import random
import actions
import buildinfo
import sys


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
       b. A server that listens to a certain port and starts a SseHTTPRequestHandler for every incoming
          connection
    """

    # Responsibility 1: provide factory:
    if sys.version_info[0] == 2:
        factory = ("tweetprocessor", "publisher")
        SseHTTPServer.SseHTTPRequestHandler.event_queue_factory = factory
    else:
        SseHTTPServer.SseHTTPRequestHandler.event_queue_factory = publisher

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

    # All responsibilities taken care of. Wait for the ECA rule engine to
    # finish:
    queue_filler.join()

MYQUEUE = [{"event": "test", "data": ["Line 1 of first message.",
                                      "Line 2 of first message."]},
           {"event": "test", "data": ["Line 1 of second message.",
                                      "Line 2 of second message."]}
          ]

BUILDINFO = buildinfo.get_buildinfo(__file__)


def publisher(listener_id, action):
    """Event source factory for SseHTTPServer.SseHTTPRequestHandler."""
    if action == "subscribe":
        return publisher_subscribe(listener_id)
    else:
        publisher_unsubscribe(listener_id)


def publisher_subscribe(listener_id):
    memusage_chart_options = {"chart": {"type": "spline",
                                         "animation": "Highcharts.svg"
                                       },
                               "title": {"text": "Max RSS of server"},
                               "xAxis": {"type": "datetime",
                                         "tickPixelInterval": 150
                                        },
                               "yAxis": {"title": {"text": "Max RSS in kB"},
                                         "plotLines": [{
                                                        "value": 0,
                                                        "width": 1,
                                                        "color": "#808080"
                                                        }]
                                         },
                               "series": [{"name": "maxrss",
                                           "data": []}]
                               }

    listeners_chart_options = {"chart": {"type": "spline",
                                         "animation": "Highcharts.svg"
                                         },
                               "title": {"text": "Number of listeners"},
                               "xAxis": {"type": "datetime",
                                         "tickPixelInterval": 150
                                         },
                               "yAxis": {"title": {"text": "Listeners"},
                                         "plotLines": [{
                                                        "value": 0,
                                                        "width": 1,
                                                        "color": "#808080"
                                                        }]
                                         },
                               "series": [{"name": "Listeners",
                                           "data": [{"x": (int(time.time()) - 1)
                                                     * 1000, "y":
                                                     random.random()},
                                                    {"x": int(time.time()) *
                                                     1000, "y":
                                                     random.random()}]}]
                               }

    for index in range(-19, 0):
        new_point = {"x": (int(time.time()) + index) * 1000,
                     "y": random.random()}
        memusage_chart_options["series"][0]["data"].append(new_point)

#     for index in range(-19, 0):
#         new_point = {"x": (int(time.time()) + index) * 1000,
#                      "y": random.random()}
#         listeners_chart_options["series"][0]["data"].append(new_point)

    _new_queue = queue.Queue()
    _new_queue.put(actions.send_buildinfo(BUILDINFO))
    _new_queue.put(actions.create_alert_gadget("cell0", "myAlerter", "Alert!"))
    _new_queue.put(actions.create_alert_gadget("cell4", "serverinfo",
                                               "Server information"))
    _new_queue.put(actions.alert("Server started!", "serverinfo"))
    _new_queue.put(actions.create_general_chart("cell1", "memusage",
                                                "Server max RSS",
                                                memusage_chart_options))
    _new_queue.put(actions.create_general_chart("cell2", "listeners",
                                                "Number of listeners",
                                                listeners_chart_options))
    # Thanks to Python's Global Interpreter Lock, the following is atomic and
    # will not corrupt the queue, even if multiple threads subscribe at the
    # "same" time
    LISTENERS[listener_id] = _new_queue
    if not EVENT.is_set():
        EVENT.set()
    return _new_queue


def publisher_unsubscribe(listener_id):
    try:
        del LISTENERS[listener_id]
        EVENT.clear()
    except KeyError:
        pass


LISTENERS = {}

EVENT = threading.Event()


class QueueFiller(threading.Thread):

    """Thread class that fills queue with heartbeat messages (one per second)

    Module 1.1 in the INF program doesn't teach classes, so we try to avoid
    them. Maybe the standard library allows to just run a function in a thread.
    """

    def __init__(self):
        threading.Thread.__init__(self)
        self.logger = logging.getLogger(__name__)

    def _send_to_all_listeners(self, message):
        for count in LISTENERS:
            LISTENERS[count].put(message)

    def run(self):
        while True:
            EVENT.wait()
            self.logger.info("QueueuFiller: started in thread %s.", self.ident)
            self._send_to_all_listeners(actions.message("queueuFiller: started in "
                                                        "server thread %s." %
                                                        self.ident))
            alert_counter = 0
            while len(LISTENERS) > 0:
                self.logger.info("QueueFiller: %s listeners, %s threads.",
                      len(LISTENERS), threading.active_count())
                self._send_to_all_listeners(actions.add_point("memusage",
                                                    int(time.time()) * 1000,
                                                    random.random()))
                self._send_to_all_listeners(actions.add_point("listeners",
                                                    int(time.time()) * 1000,
                                                    random.random()))
                if random.random() > .9:
                    alert_counter += 1
                    self._send_to_all_listeners(actions.alert("Random alert %s!" %
                                                              alert_counter,
                                                              "myAlerter"))
                time.sleep(1)
            self.logger.info("QueueFiller: stopped in thread %s.", self.ident)

if __name__ == '__main__':
    pass
