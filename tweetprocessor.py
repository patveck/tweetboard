'''
Created on 19 jul. 2013

@author: Pascal van Eck
'''

import SseHTTPServer
import queuefiller
import queue
import threading
import actions
import buildinfo


# Module 1.1 in the INF program doesn't teach classes, so we try to avoid
# them. That's why we use three globals, and a classless publish/subscribe
# mechanism.

BUILDINFO = buildinfo.get_buildinfo(__file__)

LISTENERS = {}

EVENT = threading.Event()


def process_tweets(port):
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

    # Responsibility 1: provide factory. This works only on Python 3 because it
    # depends on new-style classes. See older versions in Github for idiom to
    # make it work on Python 2.7.
    SseHTTPServer.SseHTTPRequestHandler.event_queue_factory = publisher

    # Responsibility 2a: start ECA rule engine, which is assumed to be a
    # subclass of threading.Thread. As a thread, it is assumed to wait until
    # EVENT is set before it actually starts generating messages. Currently, we
    # use a test stub for the ECA rule engine called queueFiller.
    queue_filler = queuefiller.QueueFiller(_send_to_all_listeners,
                                           _listener_length, EVENT)
    queue_filler.start()

    # Responsibility 2b: start server
    httpd = SseHTTPServer.SseHTTPServer(("", port),
                            SseHTTPServer.SseHTTPRequestHandler)
    httpd.serve_forever()

    # All responsibilities taken care of. Wait for the ECA rule engine to
    # finish:
    queue_filler.join()


def publisher(listener_id, action):
    """Event source factory for SseHTTPServer.SseHTTPRequestHandler."""
    if action == "subscribe":
        return publisher_subscribe(listener_id)
    else:
        publisher_unsubscribe(listener_id)


def publisher_subscribe(listener_id):
    """Subscribe a new listener.

    Args:
        listener_id: string that identifies the new listeners.

    Returns:
        new queue.Queue instance from which the listener can get messages.
    """

    _new_queue = queue.Queue()

    # At least, we want new listeners to know who we are, so the first message
    # we put in the queue is our own identification:
    _new_queue.put(actions.send_buildinfo(BUILDINFO))

    # We proceed with filling the queue with some initial test data:
    queuefiller.put_initial_messages(_new_queue)

    # We now register the new queue in our LISTENERS dict. Remember that this
    # function is intended to be used as a callback and will be called from a
    # thread. Thanks to Python's Global Interpreter Lock, the following is
    # atomic and will not corrupt the queue, even if multiple threads subscribe
    # at the "same" time

    LISTENERS[listener_id] = _new_queue

    # Threads that fill the queue are assumed to wait until EVENT is set.
    # Currently, Queuefiller is honoring that assumption.
    if not EVENT.is_set():
        EVENT.set()

    return _new_queue


def publisher_unsubscribe(listener_id):
    try:
        del LISTENERS[listener_id]
        EVENT.clear()
    except KeyError:
        pass


def _send_to_all_listeners(message):
    for key in LISTENERS:
        LISTENERS[key].put(message)


def _listener_length():
    return len(LISTENERS)


if __name__ == '__main__':
    print("Starting server on port 7737.")
    process_tweets(7737)
