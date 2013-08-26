'''
Created on 22 jul. 2013

@author: patveck
'''
import unittest
import actions
import json


class Test(unittest.TestCase):

    def test_add_point(self):
        self.assertEqual(actions.add_point("chart1", 4, 5),
                         {"event": "addpoint",
                          "data": ['{"X":4,"Y":5,"chartID":"chart1"}']},
                         "Message should exactly be like second arg.")

    def test_add_point_wrong_chartid(self):
        self.assertEqual(actions.add_point(1, 2, 3),
                         {"event": "message",
                          "data": ['{"messageText":"Python function add_point '
                          'called with wrong chart_id type."}']},
                         "Message should exactly be like second arg.")

    def test_add_point_empty_chartid(self):
        self.assertEqual(actions.add_point("", 2, 3),
                         {"event": "message",
                          "data": ['{"messageText":"Python function add_point '
                          'called with empty chart_id."}']},
                         "Message should exactly be like second arg.")

    def test_add_point_wrong_x_coord_str(self):
        self.assertEqual(actions.add_point("one", "two", 12.0),
                         {"event": "message",
                          "data": ['{"messageText":"Python function add_point '
                          'called with wrong x_coord type."}']},
                         "Message should exactly be like second arg (string).")

    def test_add_point_wrong_x_coord_bool(self):
        self.assertEqual(actions.add_point("one", True, 12.0),
                         {"event": "message",
                          "data": ['{"messageText":"Python function add_point '
                          'called with wrong x_coord type."}']},
                         "Message should exactly be like second arg (bool).")

    def test_add_point_wrong_y_coord_str(self):
        self.assertEqual(actions.add_point("one", 2, "three"),
                         {"event": "message",
                          "data": ['{"messageText":"Python function add_point '
                          'called with wrong y_coord type."}']},
                         "Message should exactly be like second arg (string).")

    def test_add_point_wrong_y_coord_bool(self):
        self.assertEqual(actions.add_point("one", 2, False),
                         {"event": "message",
                          "data": ['{"messageText":"Python function add_point '
                          'called with wrong y_coord type."}']},
                         "Message should exactly be like second arg (bool).")

    def test_message(self):
        self.assertEqual(actions.message("This is a message."),
                         {"event": "message",
                          "data": ['{"messageText":"This is a message."}']},
                         "Message should be exactly like second arg.")

    def test_create_alert_gadget(self):
        self.assertEqual(actions.create_alert_gadget("cell0", "alertgadget",
                                                     "My alerts"),
                         {"event": "createAlertGadget",
                          "data": ['{"cell":"cell0","id":"alertgadget","title":"My alerts"}']},
                         "Message should be exactly like second arg.")

    def test_alert(self):
        self.assertEqual(actions.alert("This is an alert.", "alertgadget"),
                         {"event": "alert",
                          "data": ['{"alertText":"This is an alert.",'
                                   '"id":"alertgadget"}']},
                         "Message should be exactly like second arg.")

    def test_create_general_chart(self):
        chart_options = {"title": {"text": "Browser market shares"},
                         "series": [{"type": "pie",
                                     "name": "Browser share",
                                     "data": [["Firefox", 45.0],
                                              ["IE", 26.8],
                                              ["Chrome", 12.8],
                                              ["Safari", 8.5],
                                              ["Opera", 6.2],
                                              ["Others", 0.7]
                                              ]}]}
        self.assertEqual(actions.create_general_chart("cell1", "chart1",
                                                      "My chart",
                                                      chart_options),
                         {"event": "createChart",
                          "data": [json.dumps({"cell": "cell1", "id": "chart1",
                                               "title": "My chart",
                                               "options": chart_options},
                                              sort_keys=True,
                                              separators=(',', ':'))]},
                         "Message should be exactly like second arg.")

    def test_create_maps_gadget(self):
        map_options = {"user": {"name": "Pascal"},
                      "text": "This is my tweet"}
        self.assertEqual(actions.create_maps_gadget("cell0", "myMap", "aTitle",
                                                    map_options),
                         {"event": "createMapsGadget",
                          "data": [json.dumps({"cell": "cell0", "id": "myMap",
                                               "title": "aTitle",
                                               "mapConfig": map_options},
                                              sort_keys=True,
                                              separators=(',', ':'))]},
                         "Message should be exactly like second arg.")

    def test_add_maps_marker(self):
        self.assertEqual(actions.add_maps_marker("myMap", 31.3, 52.4, "NL"),
                         {"event": "addMapsMarker",
                          "data": ['{"id":"myMap","lat":31.3,"long":52.4,'
                                   '"text":"NL"}']},
                         "Message should be exactly like second arg.")

    def test_create_tweetlist_gadget(self):
        self.assertEqual(actions.create_tweetlist_gadget("cell0", "myMap",
                                                         "Interesting tweets"),
                         {"event": "createTweetlistGadget",
                          "data": ['{"cell":"cell0","id":"myMap",'
                                   '"title":"Interesting tweets"}']},
                         "Message should be exactly like second arg.")

    def test_add_tweetlist_tweet(self):
        tweet_data = {"user": {"name": "Pascal"},
                      "text": "This is my tweet"}
        self.assertEqual(actions.add_tweetlist_tweet("myTweetlist", tweet_data),
                         {"event": "addTweet",
                          "data": [json.dumps({"id": "myTweetlist",
                                               "tweet": tweet_data},
                                              sort_keys=True,
                                              separators=(',', ':'))]},
                         "Message should be exactly like second arg.")

    def test_buildinfo(self):
        self.assertEqual(actions.send_buildinfo({"branch": "master",
                                                 "commit": "084f7a45"}),
                         {"event": "buildInfo",
                          "data": [json.dumps({"branch": "master",
                                              "commit": "084f7a45"},
                                             sort_keys=True,
                                             separators=(',', ':'))]},
                         "Build info not properly converted.")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_add_point']
    unittest.main()
