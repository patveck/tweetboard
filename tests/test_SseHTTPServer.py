"""test_SseHTTPServer: unit tests for SSE request handler.

The purpose of this file is to unit test SseHTTPRequestHandler, which is actually a bit complicated
because the great-great-grandfather of this class does a lot of work in its constructor. I.e., this
great-great grandfather already calls nearly all units of SseHTTPRequestHandler as part of its
constructor, while ideally one would like to test those units one by one.

Created on 11 jul. 2013

@author: Pascal van Eck
"""

import unittest
from unittest.mock import MagicMock, patch
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
        SseHTTPServer.SseHTTPRequestHandler.event_queue_factory = self.subscribe

    def subscribe(self, listener_id):
        return self.test_queue

    def test_classVars(self):
        self.assertEqual(SseHTTPServer.SseHTTPRequestHandler.eventsource_path, "/events", "Default events path not equal to /events.")
        self.assertIsNotNone(SseHTTPServer.SseHTTPRequestHandler.event_queue_factory, "Event source factory not set.")

    def test_serveIndex(self):
        MyMockSocket._reply_data = [b"GET / HTTP/1.1", b"Host: localhost:7737", b""]
        request = MyMockSocket()
        with patch("http.server.SimpleHTTPRequestHandler.do_GET") as mocked_SimpleHTTPRequestHandler_do_GET:
            self.handler = SseHTTPServer.SseHTTPRequestHandler(request, ("127.0.0.1", "7737"), self.server)
            mocked_SimpleHTTPRequestHandler_do_GET.assert_called_once_with(self.handler)

    def test_serveEvents(self):
        self.test_queue.put({"event": "test", "data": ["Line 1 of first message.", "Line 2 of first message."]})
        self.test_queue.put({"event": "terminate", "data": ["End of event stream."]})
        MyMockSocket._reply_data = [b"GET /events HTTP/1.1", b"Host: localhost:7737", b""]
        request = MyMockSocket()
        self.handler = SseHTTPServer.SseHTTPRequestHandler(request, ("127.0.0.1", "7737"), self.server)
        self.response_string = str(self.handler.response_value, "utf-8")
        self.assertRegex(self.response_string, "^HTTP/1.0 200 OK", "Response should start with HTTP/1.0 200 OK.")
        self.assertRegex(self.response_string, "Content-type: text/event-stream", "Response should contain proper content-type")
        self.assertRegex(self.response_string, "id: 1\\r\\nevent: test\\r\\ndata: Line 1 of first message\.\\r\\ndata: Line 2 of first message\.", "Response should contain first message.")
        self.assertRegex(self.response_string, "id: 2\\r\\nevent: terminate\\r\\ndata: End of event stream\.", "Response should contain terminate message.")

    def test_validMessage(self):
        self.test_queue.put({"event": "terminate", "data": ["End of event stream."]})
        MyMockSocket._reply_data = [b"GET /events HTTP/1.1", b"Host: localhost:7737", b""]
        request = MyMockSocket()
        self.handler = SseHTTPServer.SseHTTPRequestHandler(request, ("127.0.0.1", "7737"), self.server)
        _message = {"event": "test", "data": ["Line 1 of first message.", "Line 2 of first message."]}
        self.assertTrue(self.handler._check_message(_message), "Valid message, so should have returned True.")

    def test_invalidMessageNoEvent(self):
        self.test_queue.put({"event": "terminate", "data": ["End of event stream."]})
        MyMockSocket._reply_data = [b"GET /events HTTP/1.1", b"Host: localhost:7737", b""]
        request = MyMockSocket()
        self.handler = SseHTTPServer.SseHTTPRequestHandler(request, ("127.0.0.1", "7737"), self.server)
        _message = {"data": ["Line 1 of first message.", "Line 2 of first message."]}
        self.assertFalse(self.handler._check_message(_message), "Message dict has no event key.")

    def test_invalidMessageNoData(self):
        self.test_queue.put({"event": "terminate", "data": ["End of event stream."]})
        MyMockSocket._reply_data = [b"GET /events HTTP/1.1", b"Host: localhost:7737", b""]
        request = MyMockSocket()
        self.handler = SseHTTPServer.SseHTTPRequestHandler(request, ("127.0.0.1", "7737"), self.server)
        _message = {"event": "test"}
        self.assertFalse(self.handler._check_message(_message), "Message dict has no data key.")

    def test_invalidMessageEventWrongType(self):
        self.test_queue.put({"event": "terminate", "data": ["End of event stream."]})
        MyMockSocket._reply_data = [b"GET /events HTTP/1.1", b"Host: localhost:7737", b""]
        request = MyMockSocket()
        self.handler = SseHTTPServer.SseHTTPRequestHandler(request, ("127.0.0.1", "7737"), self.server)
        _message = {"event": 123, "data": ["I am event 123."]}
        self.assertFalse(self.handler._check_message(_message), "Message event is wrong type.")

    def test_invalidMessageEmptyEvent(self):
        self.test_queue.put({"event": "terminate", "data": ["End of event stream."]})
        MyMockSocket._reply_data = [b"GET /events HTTP/1.1", b"Host: localhost:7737", b""]
        request = MyMockSocket()
        self.handler = SseHTTPServer.SseHTTPRequestHandler(request, ("127.0.0.1", "7737"), self.server)
        _message = {"event": "", "data": ["I am an empty event type."]}
        self.assertFalse(self.handler._check_message(_message), "Message event is empty string.")

    def test_invalidMessageDataWrongType(self):
        self.test_queue.put({"event": "terminate", "data": ["End of event stream."]})
        MyMockSocket._reply_data = [b"GET /events HTTP/1.1", b"Host: localhost:7737", b""]
        request = MyMockSocket()
        self.handler = SseHTTPServer.SseHTTPRequestHandler(request, ("127.0.0.1", "7737"), self.server)
        _message = {"event": "test", "data": "I am just a string."}
        self.assertFalse(self.handler._check_message(_message), "Message data is not a list.")

    def test_invalidMessageEmptyData(self):
        self.test_queue.put({"event": "terminate", "data": ["End of event stream."]})
        MyMockSocket._reply_data = [b"GET /events HTTP/1.1", b"Host: localhost:7737", b""]
        request = MyMockSocket()
        self.handler = SseHTTPServer.SseHTTPRequestHandler(request, ("127.0.0.1", "7737"), self.server)
        _message = {"event": "test", "data": []}
        self.assertFalse(self.handler._check_message(_message), "Message data is empty list.")

    def test_send_message1(self):
        self.test_queue.put({"event": "terminate", "data": ["End of event stream."]})
        MyMockSocket._reply_data = [b"GET /events HTTP/1.1", b"Host: localhost:7737", b""]
        request = MyMockSocket()
        self.handler = SseHTTPServer.SseHTTPRequestHandler(request, ("127.0.0.1", "7737"), self.server)
        self.handler.wfile = io.BytesIO()
        self.handler._send_message({"event": "test", "data": ["Line 1."]}, 123)
        self.response_string = str(self.handler.wfile.getvalue(), "utf-8")
        self.assertEqual(self.response_string, "id: 123\r\nevent: test\r\ndata: Line 1.\r\n\r\n", "String representation of message not correct.")

    def test_send_message2(self):
        self.test_queue.put({"event": "terminate", "data": ["End of event stream."]})
        MyMockSocket._reply_data = [b"GET /events HTTP/1.1", b"Host: localhost:7737", b""]
        request = MyMockSocket()
        self.handler = SseHTTPServer.SseHTTPRequestHandler(request, ("127.0.0.1", "7737"), self.server)
        self.handler.wfile = io.BytesIO()
        self.handler._send_message({"event": "test", "data": ["", ""]}, 123)
        self.response_string = str(self.handler.wfile.getvalue(), "utf-8")
        self.assertEqual(self.response_string, "id: 123\r\nevent: test\r\ndata: \r\ndata: \r\n\r\n", "String representation of message not correct.")

    def test_eventloop(self):
        self.test_queue.put({"event": "terminate", "data": ["End of event stream."]})
        MyMockSocket._reply_data = [b"GET /events HTTP/1.1", b"Host: localhost:7737", b""]
        request = MyMockSocket()
        self.handler = SseHTTPServer.SseHTTPRequestHandler(request, ("127.0.0.1", "7737"), self.server)
        self.handler._check_message = MagicMock(return_value=True)
        self.handler._send_message = MagicMock()
        self.test_queue.put({"event": "terminate", "data": ["End of event stream."]})
        self.handler._send_events()
        self.handler._send_message.assert_called_once_with({"event": "terminate", "data": ["End of event stream."]}, 1)

if __name__ == "__main__":
    unittest.main()
