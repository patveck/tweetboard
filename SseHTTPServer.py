"""SseHTTPRequestHandler: HTTP GET request handler for server-sent events.

SseHTTPRequestHandler is a pure Python class that serves server-sent events to web browsers. It is only dependent
on standard library modules.

See http://dev.w3.org/html5/eventsource/

Created on 31 mei 2013

@author: Pascal van Eck

"""


__version__ = "0.1"

import http.server
import threading
import sys
import logging
import io


class SseHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):

    """HTTP GET request handler that serves a stream of event messages according to the SSE W3C recommendation.

    """

    server_version = "SseHTTP/" + __version__

    eventsource_path = "/events"

    event_queue_factory = None

    def setup(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info("SseHTTPRequestHandler(Thread-%s): setup() called", threading.current_thread().ident)
        http.server.SimpleHTTPRequestHandler.setup(self)

    def finish(self):
        self.logger.info("SseHTTPRequestHandler(Thread-%s): finish() called", threading.current_thread().ident)
        if type(self.wfile) == io.BytesIO:
            self.response_value = self.wfile.getvalue()
            self.logger.debug("SseHTTPRequestHandler: response is %s", str(self.response_value))
        http.server.SimpleHTTPRequestHandler.finish(self)

    def do_GET(self):
        """Serve a GET request. If and only if the request is for path eventsource_path (by default: /events),
        then serve events according to the SSE W3C recommendation. Otherwise, serve files by delegating to
        SimpleHTTPServer from the Python standard library.
        """
        if self.path == SseHTTPRequestHandler.eventsource_path:
            self.send_events()
        else:
            http.server.SimpleHTTPRequestHandler.do_GET(self)

    def send_events(self):
        """Common code for GET and HEAD commands.

               This sends the response code and MIME headers.

        """

        if SseHTTPRequestHandler.event_queue_factory is None:
            self.logger.critical("SseHTTPRequestHandler(Thread-%s): event_queue_factory not set", threading.current_thread().ident)
            exit()

        self._event_queue = SseHTTPRequestHandler.event_queue_factory("Thread-%s" % threading.current_thread().ident)
        logging.info("SseHTTPRequestHandler(Thread-%s): registered queue, start sending events", threading.current_thread().ident)
        self.send_response(200)
        self.send_header("Content-type", "text/event-stream")
        self.end_headers()
        _message_number = 0
        _stop = False
        while not _stop:
            _message_number += 1
            try:
                if self.wfile.closed:
                    raise RuntimeError("Response object closed.")
                _message_contents = self._event_queue.get()
                self.wfile.write(("id: %s\r\n" % _message_number).encode('UTF-8', 'replace'))
                self.wfile.write(("event: %s\r\n" % _message_contents["event"]).encode('UTF-8', 'replace'))
                for _line in _message_contents["data"]:
                    self.wfile.write(("data: %s\r\n" % _line).encode('UTF-8', 'replace'))
                self.wfile.write(b"\r\n")
                self.wfile.flush()
                if _message_contents["event"] == "terminate":
                    _stop = True
            except IOError as e:
                logging.error("_SseSender(Thread-{0}): I/O error({1}): {2}".format(threading.current_thread().ident, e.errno, e.strerror))
                if e.errno == 10053:
                    _stop = True
            except:
                logging.error("_SseSender: Unexpected error:", sys.exc_info()[0])


def test(HandlerClass=SseHTTPRequestHandler,
         ServerClass=http.server.HTTPServer):
    http.server.test(HandlerClass, ServerClass)


if __name__ == '__main__':
    test()
