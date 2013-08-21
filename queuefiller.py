'''
Created on 19 aug. 2013

@author: Pascal van Eck
'''

import threading
import time
import random
import logging
import actions


class QueueFiller(threading.Thread):

    """Thread class that fills queue with heartbeat messages (one per second)
    """

    my_queue = [{"event": "test", "data": ["Line 1 of first message.",
                                          "Line 2 of first message."]},
                {"event": "test", "data": ["Line 1 of second message.",
                                          "Line 2 of second message."]}
               ]

    def __init__(self, publisher_callback, num_of_listeners_callback, event):
        threading.Thread.__init__(self)
        self.publish = publisher_callback
        self.number_of_listeners = num_of_listeners_callback
        self.event = event
        for message in QueueFiller.my_queue:
            self.publish(message)
        self.logger = logging.getLogger(__name__)

    def run(self):
        while True:
            self.event.wait()
            self.logger.info("QueueuFiller: started in thread %s.", self.ident)
            self.publish(actions.message("queueuFiller: started in "
                                                        "server thread %s." %
                                                        self.ident))
            alert_counter = 0
            while self.number_of_listeners() > 0:
                self.logger.info("QueueFiller: %s listeners, %s threads.",
                      self.number_of_listeners(), threading.active_count())
                self.publish(actions.add_point("mychart",
                                                        int(time.time()) * 1000,
                                                        random.random()))
                if random.random() > .9:
                    alert_counter += 1
                    self.publish(actions.alert("Random alert %s!" %
                                                              alert_counter,
                                                              "myAlerter"))
                time.sleep(1)
            self.logger.info("QueueFiller: stopped in thread %s.", self.ident)


def put_initial_messages(_new_queue):
    _new_queue.put(actions.create_alert_gadget("cell0", "myAlerter"))
    _new_queue.put(actions.create_alert_gadget("cell5", "serverinfo"))
    _new_queue.put(actions.alert("Server started!", "serverinfo"))
