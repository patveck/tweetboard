u'''
Created on 22 jul. 2013

@author: patveck
'''

import json
import numbers


def _serialize(my_str):
    u"""Return a JSON version of str."""
    return json.dumps(my_str, sort_keys=True, separators=(u',', u':'))


def add_point(chart_id, x_coord, y_coord):
    u"""Create message that adds point to graph in dashboard"""
    if not type(chart_id) is unicode:
        return message(u"Python function add_point called with wrong chart_id "
                       u"type.")
    if chart_id == u"":
        return message(u"Python function add_point called with empty chart_id.")
    # In the type hierarchy, numbers.Integral instances are also number.Real
    # instances, but not the other way around. Boolean values are instances
    # of numbers.Integral
    if not (isinstance(x_coord, numbers.Real) and
             not type(x_coord) is bool):
        return message(u"Python function add_point called with wrong x_coord "
                       u"type.")
    if not (isinstance(y_coord, numbers.Real) and
             not type(y_coord) is bool):
        return message(u"Python function add_point called with wrong y_coord "
                       u"type.")
    return {u"event": u"addpoint",
            u"data": [_serialize({u"chartID": chart_id,
                                 u"X": x_coord, u"Y": y_coord})]}


def message(message_text):
    u"""Create message that displays a message (not an alert) in dashboard"""
    return {u"event": u"message",
            u"data": [_serialize({u"messageText": message_text})]}


def create_alert_gadget(cell, gadget_id):
    u"""Create a gadget that shows alerts

    Adds an alert gadget to the current jQuery selection. The selection is
    decorated with CSS class "alertgadget-cell", the gadget contents with
    CSS class "alertgadget". Initially, the gadget is not visible (in CSS
    terms: its ""visibility" is "hidden" and its "height" is "0px".
    """
    return {u"event": u"createAlertGadget",
            u"data": [_serialize({u"id": gadget_id, u"cell": cell})]}


def alert(alert_text, gadget_id):
    u"""Show an alert (not a message) in the alert gadget identified by id

    Adds an alert to the alert gadget identified by id. If the gadget is
    currently not visible, it is made visible. The alert disappears after
    8 seconds. If it was the last alert to be displayed, the entire gadget is
    made invisible.
    """
    return {u"event": u"alert",
            u"data": [_serialize({u"id": gadget_id, u"alertText": alert_text})]}


def create_general_chart(chart_id, chart_options):
    u"""Create message that creates a new chart in dashboard"""
    return {u"event": u"createChart",
            u"data": [_serialize({u"chartID": chart_id,
                                 u"chartOptions": chart_options})]}


def send_buildinfo(buildinfo):
    u"""Create message that informs client of its version information"""
    return {u"event": u"buildInfo",
            u"data": [_serialize(buildinfo)]}


if __name__ == u'__main__':
    pass
