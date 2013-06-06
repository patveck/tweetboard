import logging

def action1(e):
    logging.info('Action action1 invoked.')

myRules = [
    {
        'id': 'regel1',
        'docstring': '',
        'event': 'tweet_received',
        'condition': lambda e: e.hashtag == '#bata',
        'action': lambda e: action1(e)
    },
    {
        'id': 'regel2',
        'docstring': '',
        'event': 'tweet_received',
        'condition': lambda e: follower_of(e.sender, '@patveck'),
        'action': lambda e: do_something(e)
    }
]

def dashboardAlert(message):
    """Push an alert to the Twitter dashboard.

    :param message: the text to display in the alert
    :type message: string
    :returns: nothing

    """

def dashboardAddPoint(chart, x, y):
    """Push one data point to existing chart in the Twitter dashboard.

    Keyword arguments:
    chart -- the chart, identified as text string
    x -- x value of data point
    y -- y value of data point

    """

