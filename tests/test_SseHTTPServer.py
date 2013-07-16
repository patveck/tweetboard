"""test_SseHTTPServer: unit tests for SSE request handler.

The purpose of this file is to unit test SseHTTPRequestHandler, which is actually a bit complicated
because the great-great-grandfather of this class does a lot of work in its constructor. I.e., this
great-great grandfather already calls nearly all units of SseHTTPRequestHandler as part of its
constructor, while ideally one would like to test those units one by one.



Created on 11 jul. 2013

@author: Pascal van Eck
"""

import unittest
from unittest.mock import MagicMock
import test.mock_socket
import SseHTTPServer
import queue
import logging
import io


class MyMockFile(test.mock_socket.MockFile):

    def __init__(self, lines):
        self.closed = False
        self.lines = lines

    def readline(self, bufsize):
        return self.lines.pop(0) + b'\r\n'


class MyMockSocket(test.mock_socket.MockSocket):

    _reply_data = []

    def __init__(self):
        self.output = []
        self.lines = []
        if MyMockSocket._reply_data:
            for i in MyMockSocket._reply_data:
                self.lines.append(i)
        self.conn = None
        self.timeout = None

    def makefile(self, mode='r', bufsize=-1):
        if mode == "rb":
            handle = MyMockFile(self.lines)
            return handle
        else:
            handle = io.BytesIO()
            return handle


class Test(unittest.TestCase):

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        self.server = MagicMock(name="server")
        self.test_queue = queue.Queue()
        self.test_queue.put({"event": "test", "data": ["Line 1 of first message.", "Line 2 of first message."]})
        self.test_queue.put({"event": "terminate", "data": ["End of event stream."]})
        SseHTTPServer.SseHTTPRequestHandler.event_queue_factory = self.subscribe

    def subscribe(self, listener_id):
        return self.test_queue

    def test_classVars(self):
        self.assertEqual(SseHTTPServer.SseHTTPRequestHandler.eventsource_path, "/events", "Default events path not equal to /events.")
        self.assertIsNotNone(SseHTTPServer.SseHTTPRequestHandler.event_queue_factory, "Event source factory not set.")

    def test_serveIndex(self):
        MyMockSocket._reply_data = [b"GET / HTTP/1.1", b"Host: localhost:7737", b""]
        request = MyMockSocket()
        self.handler = SseHTTPServer.SseHTTPRequestHandler(request, ("127.0.0.1", "7737"), self.server)
        self.response_string = str(self.handler.response_value, "utf-8")
        self.assertRegex(self.response_string, "^HTTP/1.0 200 OK", "Response should start with HTTP/1.0 200 OK.")
        self.assertRegex(self.response_string, "Content-type: text/html", "Response should contain proper content-type")
        self.assertRegex(self.response_string, "<title>Pascal", "Response should contain <title>Pascal.")

    def test_serveEvents(self):
        MyMockSocket._reply_data = [b"GET /events HTTP/1.1", b"Host: localhost:7737", b""]
        request = MyMockSocket()
        self.handler = SseHTTPServer.SseHTTPRequestHandler(request, ("127.0.0.1", "7737"), self.server)
        self.response_string = str(self.handler.response_value, "utf-8")
        self.assertRegex(self.response_string, "^HTTP/1.0 200 OK", "Response should start with HTTP/1.0 200 OK.")
        self.assertRegex(self.response_string, "Content-type: text/event-stream", "Response should contain proper content-type")
        self.assertRegex(self.response_string, "id: 1\\r\\nevent: test\\r\\ndata: Line 1 of first message\.\\r\\ndata: Line 2 of first message\.", "Response should contain first message.")
        self.assertRegex(self.response_string, "id: 2\\r\\nevent: terminate\\r\\ndata: End of event stream\.", "Response should contain terminate message.")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
