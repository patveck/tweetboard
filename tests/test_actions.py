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

    def test_add_point_wrong_x_coord(self):
        self.assertEqual(actions.add_point("one", "two", 12.0),
                         {"event": "message",
                          "data": ['{"messageText":"Python function add_point '
                          'called with wrong x_coord type."}']},
                         "Message should exactly be like second arg.")

    def test_add_point_wrong_y_coord(self):
        self.assertEqual(actions.add_point("one", 2, "three"),
                         {"event": "message",
                          "data": ['{"messageText":"Python function add_point '
                          'called with wrong y_coord type."}']},
                         "Message should exactly be like second arg.")

    def test_message(self):
        self.assertEqual(actions.message("This is a message."),
                         {"event": "message",
                          "data": ['{"messageText":"This is a message."}']},
                         "Message should be exactly like second arg.")

    def test_alert(self):
        self.assertEqual(actions.alert("This is an alert."),
                         {"event": "alert",
                          "data": ['{"alertText":"This is an alert."}']},
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
        self.assertEqual(actions.create_general_chart("chart1",
                                                      chart_options),
                         {"event": "createChart",
                          "data": [json.dumps({"chartID": "chart1",
                                               "chartOptions": chart_options},
                                              sort_keys=True,
                                              separators=(',', ':'))]},
                         "Message should be exactly like second arg.")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_add_point']
    unittest.main()
