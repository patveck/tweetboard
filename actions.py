'''
Created on 22 jul. 2013

@author: patveck
'''

import json
import numbers


class ActionWrapper:
    """Simple wrapper class for publishing action value."""
    def __init__(self, value):
        self.value = value


def _encode(value):
    """Encode the action."""
    return ActionWrapper(value)


def is_action(value):
    """check if the string is an action."""
    return isinstance(value, ActionWrapper)


def decode(wrapper):
    """Decode the action."""
    return wrapper.value


def _serialize(my_str):
    """Return a JSON version of str."""
    return json.dumps(my_str, sort_keys=True, separators=(',', ':'))


def cell_definition(id, gadget, options):
    """Handle a cell definition"""
    print('# Should handle cell_definition('+id+','+gadget+','+options+')')


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
    return _encode({"event": "addpoint",
            "data": [_serialize({"chartID": chart_id,
                                 "X": x_coord, "Y": y_coord})]})


def message(message_text):
    """Create message that displays a message (not an alert) in dashboard.

    Args:
        message_text: text of the message to be displayed.

    Returns:
        A dict with two members ("event" and "data"), with the value of "data"
        a JSON serialization of the arguments. This is the format expected by
        SseHTTPRequestHandler.
    """
    return _encode({"event": "message",
            "data": [_serialize({"messageText": message_text})]})


#
# Alert gadget actions:
#

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
    return _encode({"event": "createAlertGadget",
            "data": [_serialize({"id": gadget_id, "cell": cell,
                                 "title": gadget_title})]})


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
    return _encode({"event": "alert",
            "data": [_serialize({"id": gadget_id, "alertText": alert_text})]})


#
# Chart gadget actions:
#

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
    return _encode({"event": "createChart",
            "data": [_serialize({"id": chart_id, "cell": cell,
                                 "title": gadget_title,
                                 "options": chart_options})]})
#
# Maps gadget actions
#


def create_maps_gadget(cell, gadget_id, gadget_title, map_options):
    """Create message that creates a new Google Maps gadget in dashboard.

    This action creates a message that when received by the client creates a
    gadget that shows a Google map. We use Gmap3 (see http://gmap3.net/) as
    library to display the map; see the documentation of Gmap3 for all
    options.

    Args:
        cell:
        gadget_id:
        gadget_title:
        map_options: Python options dictionary that will be used in the call
            of the $.gmap3() function in the client; see see http://gmap3.net/
            for documentation.
    Returns:
        A dict with two members ("event" and "data"), with the value of "data"
        a JSON serialization of the arguments. This is the format expected by
        SseHTTPRequestHandler.
    """
    return _encode({"event": "createMapsGadget",
            "data": [_serialize({"cell": cell, "id": gadget_id,
                                 "title": gadget_title,
                                 "mapConfig": map_options})]})


def add_maps_marker(gadget_id, lat, long, marker_text):
    """Add a marker to an existing Google map.

    Args:
        gadget_id: String identifying the existing map to which this marker is
            to be added.
        lat: Latitude of the position of this marker on the map.
        long: Longitude of the position of this marker on the map.
        marker_text: String (can be HTML formatted) that will be displayed in an
            "infowindow" displayed on top of the marker when the mouse moves
            over it.
    Returns:
        A dict with two members ("event" and "data"), with the value of "data"
        a JSON serialization of the arguments. This is the format expected by
        SseHTTPRequestHandler.
    """
    return _encode({"event": "addMapsMarker",
            "data": [_serialize({"id": gadget_id, "lat": lat, "long": long,
                                 "text": marker_text})]})

#
# Tweetlist gadget actions
#


def create_tweetlist_gadget(cell, gadget_id, gadget_title):
    """Create message that creates a new tweetlist gadget in dashboard.

    This action creates a message that when received by the client creates a
    gadget that can show a list of tweets.

    Args:
        cell:
        gadget_id:
        gadget_title:
    Returns:
        A dict with two members ("event" and "data"), with the value of "data"
        a JSON serialization of the arguments. This is the format expected by
        SseHTTPRequestHandler.
    """
    return _encode({"event": "createTweetlistGadget",
            "data": [_serialize({"cell": cell, "id": gadget_id,
                                 "title": gadget_title})]})


def add_tweetlist_tweet(gadget_id, tweet_data):
    """Add a tweet to an existing tweet list gadget.

    Args:
        gadget_id:
        tweet_data:
    Returns:
        A dict with two members ("event" and "data"), with the value of "data"
        a JSON serialization of the arguments. This is the format expected by
        SseHTTPRequestHandler.
    """
    return _encode({"event": "addTweet",
            "data": [_serialize({"id": gadget_id, "tweet": tweet_data})]})

#
# Buildinfo action:
#


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
    return _encode({"event": "buildInfo",
            "data": [_serialize(buildinfo)]})

# IMPORTANT: any function which may be used in the ECA rule file must be defined
# in he action_function dict
action_functions = {
	"add_point" : ( 3, lambda input: lambda event: add_point(tuple(input[1](event))[0],tuple(input[1](event))[1],tuple(input[1](event))[2])),
	"message" : ( 1, lambda input: lambda event: message(tuple(input[1](event))[0])),
	"alert" : ( 3, lambda input: lambda event: alert(tuple(input[1](event))[0],tuple(input[1](event))[1]))
}

if __name__ == '__main__':
    pass
