"""Server-sent events module.

sse is a pure Python module that serves server-sent events to web browsers. It is only dependent
on standard library modules.

See http://dev.w3.org/html5/eventsource/

Created on 31 mei 2013

@author: patveck

"""


__version__ = "0.1"

import http.server
import queue
import threading
import time
import sys
import random


class SseHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):

    """HTTP GET request handler that serves a stream of event messages according to the SSE W3C recommendation.

    """

    server_version = "SseHTTP/" + __version__

    eventsource_path = "/events"

    event_queue = queue.Queue()

    def do_GET(self):
        """Serve a GET request."""
        if self.path == SseHTTPRequestHandler.eventsource_path:
            self.send_events()
        else:
            http.server.SimpleHTTPRequestHandler.do_GET(self)

    def send_events(self):
        """Common code for GET and HEAD commands.

               This sends the response code and MIME headers.

        """
        _my_name = "Thread-%s" % threading.current_thread().ident
        print("SseHTTPRequestHandler(%s): sending events" % _my_name)
        self.send_response(200)
        self.send_header("Content-type", "text/event-stream")
        self.end_headers()
        _message_number = 0
        while True:
            _message_number += 1
            try:
                if self.wfile.closed:
                    raise RuntimeError("Response object closed.")
                self.wfile.write(("id: %s\n" % _message_number).encode('UTF-8', 'replace'))
                if SseHTTPRequestHandler.event_queue.empty():
                    self.wfile.write(b"event: addpoint\n")
                    self.wfile.write(('data: {"X": %s, "Y": %s}\n' % (int(time.time()) * 1000, random.random())).encode('UTF-8', 'replace'))
                else:
                    for _line in SseHTTPRequestHandler.event_queue.get()["data"]:
                        self.wfile.write(("data: %s\n" % _line).encode('UTF-8', 'replace'))
                self.wfile.write(b"\n")
                self.wfile.flush()
            except IOError as e:
                print("_SseSender({0}): I/O error({1}): {2}".format(_my_name, e.errno, e.strerror))
            except:
                print("_SseSender: Unexpected error:", sys.exc_info()[0])
            time.sleep(1)


def test(HandlerClass=SseHTTPRequestHandler,
         ServerClass=http.server.HTTPServer):
    http.server.test(HandlerClass, ServerClass)


if __name__ == '__main__':
    test()
