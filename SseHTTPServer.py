"""Server-sent events module.

sse is a pure Python module that serves server-sent events to web browsers. It is only dependent
on standard library modules.

See http://dev.w3.org/html5/eventsource/

Created on 31 mei 2013

@author: patveck

"""


__version__ = "0.1"

import BaseHTTPServer
import SimpleHTTPServer
import Queue
import threading
import time
import sys
import random


class _SseSender(threading.Thread):

    """Helper class that sends out events from a queue

    """

    def __init__(self, wfile):
        self.wfile = wfile
        threading.Thread.__init__(self)

    def run(self):
        _message_number = 0
        while True:
            _message_number += 1
            try:
                if self.wfile.closed:
                    raise RuntimeError("Response object closed.")
                self.wfile.write("id: %s\n" % _message_number)
                if SseHTTPRequestHandler.event_queue.empty():
                    self.wfile.write("event: addpoint\n")
                    self.wfile.write('data: {"X": %s, "Y": %s}\n' % (int(time.time()) * 1000, random.random()))
                else:
                    for _line in SseHTTPRequestHandler.event_queue.get()["data"]:
                        self.wfile.write("data: %s\n" % _line)
                self.wfile.write("\n")
                self.wfile.flush()
            except IOError as e:
                print "_SseSender: I/O error({0}): {1}".format(e.errno, e.strerror)
            except:
                print "_SseSender: Unexpected error:", sys.exc_info()[0]
            time.sleep(1)


class SseHTTPRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    """HTTP GET request handler that serves a stream of event messages according to the SSE W3C recommendation.

    """

    server_version = "SseHTTP/" + __version__

    eventsource_path = "/events"

    event_queue = Queue.Queue()

    def do_GET(self):
        """Serve a GET request."""
        if self.path == SseHTTPRequestHandler.eventsource_path:
            self.send_events()
        else:
            SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

    def send_events(self):
        """Common code for GET and HEAD commands.

               This sends the response code and MIME headers.

        """
        self.send_response(200)
        self.send_header("Content-type", "text/event-stream")
        self.sseSender = _SseSender(self.wfile)
        self.sseSender.start()
        time.sleep(3600)


def test(HandlerClass=SseHTTPRequestHandler,
         ServerClass=BaseHTTPServer.HTTPServer):
    BaseHTTPServer.test(HandlerClass, ServerClass)


if __name__ == '__main__':
    test()
