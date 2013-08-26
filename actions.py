'''
Created on 22 jul. 2013

@author: patveck
'''

import json
import numbers


def _serialize(my_str):
    """Return a JSON version of str."""
    return json.dumps(my_str, sort_keys=True, separators=(',', ':'))


def add_point(chart_id, x_coord, y_coord):
    """Create message that adds point to graph in dashboard.

    Args:
        chart_id: string identifying the (existing) chart to which a point is to
            be added.
        x_coord: x-coordinate of the point to be added (integer or float).
        y_coord: y-coordinate of the point to be added (integer or float).

    Returns:
        A dict with two members ("event" and "data"), with the value of "data"
        a JSON serialization of the arguments. This is the format expected by
        SseHTTPRequestHandler.
    """
    if not type(chart_id) is str:
        return message("Python function add_point called with wrong chart_id "
                       "type.")
    if chart_id == "":
        return message("Python function add_point called with empty chart_id.")
    # In the type hierarchy, numbers.Integral instances are also number.Real
    # instances, but not the other way around. Boolean values are instances
    # of numbers.Integral
    if not (isinstance(x_coord, numbers.Real) and
             not type(x_coord) is bool):
        return message("Python function add_point called with wrong x_coord "
                       "type.")
    if not (isinstance(y_coord, numbers.Real) and
             not type(y_coord) is bool):
        return message("Python function add_point called with wrong y_coord "
                       "type.")
    return {"event": "addpoint",
            "data": [_serialize({"chartID": chart_id,
                                 "X": x_coord, "Y": y_coord})]}


def message(message_text):
    """Create message that displays a message (not an alert) in dashboard.

    Args:
        message_text: text of the message to be displayed.

    Returns:
        A dict with two members ("event" and "data"), with the value of "data"
        a JSON serialization of the arguments. This is the format expected by
        SseHTTPRequestHandler.
    """
    return {"event": "message",
            "data": [_serialize({"messageText": message_text})]}


def create_alert_gadget(cell, gadget_id, gadget_title):
    """Create a gadget that shows alerts.

    Adds an alert gadget to the current jQuery selection. The selection is
    decorated with CSS class "alertgadget-cell", the gadget contents with
    CSS class "alertgadget". Initially, the gadget is not visible (in CSS
    terms: its ""visibility" is "hidden" and its "height" is "0px".

    Args:
        cell: id of the HTML element that receives the gadget. An element with
            this id should exist in the HTML representation of the dashboard.
        gadget_id: string that will be used later on to identify this gadget.
        gadget_title: string that will be displayed in the gadget's title bar.

    Returns:
        A dict with two members ("event" and "data"), with the value of "data"
        a JSON serialization of the arguments. This is the format expected by
        SseHTTPRequestHandler.
    """
    return {"event": "createAlertGadget",
            "data": [_serialize({"id": gadget_id, "cell": cell,
                                 "title": gadget_title})]}


def alert(alert_text, gadget_id):
    """Show an alert (not a message) in the alert gadget identified by id.

    Adds an alert to the alert gadget identified by id. If the gadget is
    currently not visible, it is made visible. The alert disappears after
    8 seconds. If it was the last alert to be displayed, the entire gadget is
    made invisible.

    Args:
        alert_text: string to display as new alert in the alert gadget
            identified by gadget_id
        gadget_id: string that identifies the alert gadget to use for this alert

    Returns:
        A dict with two members ("event" and "data"), with the value of "data"
        a JSON serialization of the arguments. This is the format expected by
        SseHTTPRequestHandler.
    """
    return {"event": "alert",
            "data": [_serialize({"id": gadget_id, "alertText": alert_text})]}


def create_general_chart(cell, chart_id, gadget_title, chart_options):
    """Create message that creates a new chart in dashboard.

    Adds a chart gadget to the current jQuery selection. The selection is
    decorated with CSS class "chartgadget-cell", the gadget contents with
    CSS class "chartgadget".

    Args:
        cell: id of the HTML element that receives the gadget. An element with
            this id should exist in the HTML representation of the dashboard.
        chart_id: string that will be used later on to identify this chart.
        gadget_title: string that will be displayed in the gadget's title bar.
        chart_options: a dict containing chart options as expected by
            HighCharts.JS.

    Returns:
        A dict with two members ("event" and "data"), with the value of "data"
        a JSON serialization of the arguments. This is the format expected by
        SseHTTPRequestHandler.
    """
    return {"event": "createChart",
            "data": [_serialize({"id": chart_id, "cell": cell,
                                 "title": gadget_title,
                                 "options": chart_options})]}


def send_buildinfo(buildinfo):
    """Create message that informs client of its version information.

    Args:
        buildinfo: string to send to client, the idea is that this string
            identifies the build (e.g., in the form of a version number).

    Returns:
        A dict with two members ("event" and "data"), with the value of "data"
        a JSON serialization of the arguments. This is the format expected by
        SseHTTPRequestHandler.
    """
    return {"event": "buildInfo",
            "data": [_serialize(buildinfo)]}


if __name__ == '__main__':
    pass
