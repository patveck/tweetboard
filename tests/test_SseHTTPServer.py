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


def subscribe(listener_id):
    return queue.Queue()


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
            handle = open("servertest_out.txt", "wb")
            return handle


class Test(unittest.TestCase):

    def setUp(self):
        SseHTTPServer.SseHTTPRequestHandler.event_queue_factory = subscribe
        self.server = MagicMock(name="server")
        MyMockSocket._reply_data = [b"GET / HTTP/1.1", b"Host: localhost:7737", b""]
        request = MyMockSocket()
        self.handler = SseHTTPServer.SseHTTPRequestHandler(request, ("127.0.0.1", "123"), self.server)

    def test_classVars(self):
        self.assertEqual(SseHTTPServer.SseHTTPRequestHandler.eventsource_path, "/events", "Default events path not equal to /events.")
        self.assertIsNotNone(SseHTTPServer.SseHTTPRequestHandler.event_queue_factory, "Event source factory not set.")

    def test_serveIndex(self):
        MyMockSocket._reply_data = [b"GET / HTTP/1.1", b"Host: localhost:7737", b""]
        request = MyMockSocket()
        self.handler = SseHTTPServer.SseHTTPRequestHandler(request, ("127.0.0.1", "123"), self.server)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
