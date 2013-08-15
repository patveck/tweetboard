u"""SseHTTPRequestHandler: HTTP GET request handler for server-sent events.

SseHTTPRequestHandler is a pure Python class that serves server-sent events to
web browsers. It is only dependent on standard library modules.

See http://dev.w3.org/html5/eventsource/

Created on 31 mei 2013

@author: Pascal van Eck

"""


__version__ = u"0.1"

import CGIHTTPServer, SimpleHTTPServer, BaseHTTPServer
import SocketServer
import threading
import sys
import logging
import io
import Queue
import importlib


class SseHTTPRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    u"""HTTP GET request handler that serves a stream of event messages
    according to the SSE W3C recommendation.

    The only dependency that is not in the Python Standard Library is injected
    via a class variable called event_queue_factory.

    As per the structure of the http.server framework in the Python Standard
    Library, this class is not instantiated directly by application scripts.
    Instead, application scripts instantiate socketserver.TCPserver, providing
    this class (not an instance of this class) as an argument to the
    constructor of socketserver.TCPserver. TCPserver (actually, one of its
    ancestors) in turn instantiates this class once for every incoming
    connection.

    """

    server_version = u"SseHTTP/" + __version__

    eventsource_path = u"/events"

    event_queue_factory = None

    def __init__(self, request, client_address, server):
        self.response_value = u""
        self.logger = logging.getLogger(__name__)
        self._event_queue = None
        SimpleHTTPServer.SimpleHTTPRequestHandler.__init__(self, request,
                                                      client_address, server)

    def setup(self):
        self.logger.debug(u"SseHTTPRequestHandler(Thread-%s): setup() called",
                         threading.current_thread().ident)
        SimpleHTTPServer.SimpleHTTPRequestHandler.setup(self)

    def finish(self):
        self.logger.info(u"SseHTTPRequestHandler(Thread-%s): finish() called",
                         threading.current_thread().ident)
        if type(self.wfile) == io.BytesIO:
            self.response_value = self.wfile.getvalue()
            self.logger.debug(u"SseHTTPRequestHandler: response is %s",
                              unicode(self.response_value))
        try:
            SimpleHTTPServer.SimpleHTTPRequestHandler.finish(self)
        except:
            self.logger.warning(u"SseHTTPRequestHandler(Thread-%s): exception "
                                u"in finish()", threading.current_thread().ident)
            self._call_factory(u"unsubscribe")

    def handle_error(self, request, client_address):
        self.logger.warning(u"SseHTTPRequestHandler(Thread-%s): handle_error() "
                            u"called", threading.current_thread().ident)
        self._call_factory(u"unsubscribe")

    def do_GET(self):
        u"""Serve a GET request. If and only if the request is for path
        eventsource_path (by default: /events), then serve events according
        to the SSE W3C recommendation. Otherwise, serve files by delegating to
        SimpleHTTPServer from the Python standard library.
        """
        if self.path == SseHTTPRequestHandler.eventsource_path:
            self._start_event_stream()
        else:
            SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

    def _start_event_stream(self):
        u"""Initialize event queue, send headers, start sending events."""

        # Register with an event queue, which will be used as event source:
        self._call_factory(u"subscribe")
        self.logger.debug(u"SseHTTPRequestHandler(Thread-%s): registered queue, "
                     u"start sending events", threading.current_thread().ident)

        # Send HTTP headers:
        self.send_response(200)
        self.send_header(u"Content-type", u"text/event-stream")
        self.end_headers()

        # Start event serving loop:
        self._send_events()

    def _send_events(self):
        u"""Get message from event queue, check whether correct, and if so,
        send it to client. Repeat until message has event terminate."""
        _message_number = 0
        _stop = False
        while not _stop:
            _message_number += 1
            try:
                _message_contents = self._event_queue.get()
                if self._check_message(_message_contents):
                    self._send_message(_message_contents, _message_number)
                if _message_contents[u"event"] == u"terminate":
                    _stop = True
            except IOError, ex:
                if ex.errno == 10053 or ex.errno == 10054 or ex.errno == 32:
                    self.logger.info(u"_SseSender(Thread-{0}): "
                                     u"client closed connection.".format(
                                           threading.current_thread().ident))
                    _stop = True
                else:
                    self.logger.warning(u"_SseSender(Thread-{0}): "
                                        u"I/O error({1}): "
                              u"{2}".format(threading.current_thread().ident,
                                           ex.errno, ex.strerror))
            except:
                self.logger.error(u"_SseSender(Thread-{0}): Unexpected error: "
                              u"{1}".format(threading.current_thread().ident,
                                           sys.exc_info()[0]))
        self.logger.info(u"_SseSender(Thread-{0}): Calling unsubscribe.".format(threading.current_thread().ident))
        self._call_factory(u"unsubscribe")

    def _call_factory(self, action):
        if sys.version_info[0] == 2:
            factory_module_name = SseHTTPRequestHandler.event_queue_factory[0]
            factory_function_name = SseHTTPRequestHandler.event_queue_factory[1]
            factory_module = importlib.import_module(factory_module_name)
            factory_function = getattr(factory_module, factory_function_name)
            self._event_queue = factory_function(  # pylint: disable=E1102
                                u"Thread-%s" % threading.current_thread().ident,
                                action)
        else:
            if not hasattr(SseHTTPRequestHandler.event_queue_factory,
                           u"__call__"):
                self.logger.critical(u"SseHTTPRequestHandler(Thread-%s): "
                                     u"event_queue_factory not callable",
                                     threading.current_thread().ident)
                exit()
            self._event_queue = SseHTTPRequestHandler.event_queue_factory(  # pylint: disable=E1102
                                u"Thread-%s" % threading.current_thread().ident,
                                action)

    def _check_message(self, _message_contents):
        u"""Check whether message complies with expected format."""
        if not u"event" in _message_contents:
            self.logger.error(u"Message dict has no event key.")
            return False
        if not u"data" in _message_contents:
            self.logger.error(u"Message dict has no data key.")
            return False
        if not type(_message_contents[u"event"]) == unicode:
            self.logger.error(u"Message event is not a string.")
            return False
        if len(_message_contents[u"event"]) == 0:
            self.logger.error(u"Message event cannot be empty.")
            return False
        if not type(_message_contents[u"data"]) == list:
            self.logger.error(u"Message data is not a list.")
            return False
        if len(_message_contents[u"data"]) == 0:
            self.logger.error(u"Message data cannot be empty list.")
            return False
        return True

    def _send_message(self, _message_contents, _message_number):
        u"""Format message and send it by writing it to self.wfile."""
        if self.wfile.closed:
            raise RuntimeError(u"Response object closed.")
        self.logger.debug(u"SseHTTPRequestHandler(Thread-%s): sending message "
                     u" %s: %s.", threading.current_thread().ident,
                     _message_number, _message_contents)
        self.wfile.write((u"id: %s\r\n" %
                          _message_number).encode(u'UTF-8', u'replace'))
        self.wfile.write((u"event: %s\r\n" %
                          _message_contents[u"event"]).encode(u'UTF-8',
                                                             u'replace'))
        for _line in _message_contents[u"data"]:
            self.wfile.write((u"data: %s\r\n" %
                              _line).encode(u'UTF-8', u'replace'))
        self.wfile.write("\r\n")
        self.wfile.flush()


def test(handler_class=SseHTTPRequestHandler,
         server_class=SocketServer.ThreadingTCPServer):
    u"""Starts a server on port 8000."""
    test_queue = Queue.Queue()
    test_queue.put({u"event": u"terminate", u"data": [u"End of event stream."]})
    SseHTTPRequestHandler.event_queue_factory = lambda subscriber: test_queue
    None.test(handler_class, server_class)


if __name__ == u'__main__':
    test()
