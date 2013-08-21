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
    """Create message that adds point to graph in dashboard"""
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
    """Create message that displays a message (not an alert) in dashboard"""
    return {"event": "message",
            "data": [_serialize({"messageText": message_text})]}


#
# Alert gadget actions:
#

def create_alert_gadget(cell, gadget_id):
    """Create a gadget that shows alerts

    Adds an alert gadget to the current jQuery selection. The selection is
    decorated with CSS class "alertgadget-cell", the gadget contents with
    CSS class "alertgadget". Initially, the gadget is not visible (in CSS
    terms: its ""visibility" is "hidden" and its "height" is "0px".
    """
    return {"event": "createAlertGadget",
            "data": [_serialize({"id": gadget_id, "cell": cell})]}


def alert(alert_text, gadget_id):
    """Show an alert (not a message) in the alert gadget identified by id

    Adds an alert to the alert gadget identified by id. If the gadget is
    currently not visible, it is made visible. The alert disappears after
    8 seconds. If it was the last alert to be displayed, the entire gadget is
    made invisible.
    """
    return {"event": "alert",
            "data": [_serialize({"id": gadget_id, "alertText": alert_text})]}


#
# Chart gadget actions:
#

def create_general_chart(chart_id, chart_options):
    """Create message that creates a new chart in dashboard"""
    return {"event": "createChart",
            "data": [_serialize({"chartID": chart_id,
                                 "chartOptions": chart_options})]}

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
        map_options: see https://developers.google.com/maps/documentation/javascript/reference#MapOptions
    Returns:
    """
    return {"event": "createMapsGadget",
            "data": [_serialize({"cell": cell, "id": gadget_id,
                                 "title": gadget_title,
                                 "mapConfig": map_options})]}


def add_maps_marker(gadget_id, lat, long, marker_text):
    return {"event": "addMapsMarker",
            "data": [_serialize({"id": gadget_id, "lat": lat, "long": long,
                                 "text": marker_text})]}

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
    """
    return {"event": "createTweetlistGadget",
            "data": [_serialize({"cell": cell, "id": gadget_id,
                                 "title": gadget_title})]}


def add_tweetlist_tweet(gadget_id, tweet_data):
    return {"event": "addTweet",
            "data": [_serialize({"id": gadget_id, "tweet": tweet_data})]}

#
# Buildinfo action:
#


def send_buildinfo(buildinfo):
    """Create message that informs client of its version information"""
    return {"event": "buildInfo",
            "data": [_serialize(buildinfo)]}


if __name__ == '__main__':
    pass
