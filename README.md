TweetBoard - Twitter Dashboard for "Pearls of Computer Science" [![Build Status](https://travis-ci.org/patveck/tweetboard.png)](https://travis-ci.org/patveck/tweetboard)
---------------------------------------------------------------

Starting September 2013, the [University of Twente](http://utwente.nl/en/) gradually introduces [project-based learning](http://en.wikipedia.org/wiki/Project-based_learning) in all bachelor-level courses. Moreover, for the first course, a university-wide theme has been chosen: sports. The [Computer Science bachelor program](http://www.utwente.nl/bachelor/inf/) of University of Twente has chosen to focus on creating a Twitter monitoring dashboard for various stakeholders in the [Batavierenrace](http://en.wikipedia.org/wiki/Batavierenrace), a 185-km student relay race in which over 8000 runners participate.

In the first course in the Computer Science program, we offer a fully-functioning Twitter monitoring dashboard written in JavaScript and Python for students to configure, adapt and extend. This Github site contains the source

Getting started
---------------

TweetBoard consists of a frontend written in HTML/CSS/JavaScript and a backend written in pure Python. To run Tweetboard, execute the following two steps:

1. Start the server by running sseserver.py. On Windows, assuming that .py files are associated with the Python interpreter, this can be done by double-clicking sseserver.py. The server by default listens to port 7737.
2. Start the frontend by loading index.html in a browser. Currently, only Chrome and Firefox are known to work. Assuming that the server listens to port 7737, point your browser at [http://localhost:7737](http://localhost:7737) to start the frontend.


License
-------

TweetBoard is released under a [Creative Commons Attribution-NonCommercial 3.0 License](http://creativecommons.org/licenses/by-nc/3.0/). TweetBoard relies heavily on [Highcharts JS](http://www.highcharts.com/), a JavaScript charting library. Highcharts itself is licensed under the same license for [personal or non-profit projects](http://shop.highsoft.com/highcharts.html).  
