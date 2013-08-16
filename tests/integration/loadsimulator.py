#!/usr/local/bin/python2.7
# encoding: utf-8
'''
tests.integration.loadsimulator -- shortdesc

tests.integration.loadsimulator is a description

It defines classes_and_methods

@author:     Pascal van Eck

@copyright:  2013 organization_name. All rights reserved.

@license:    Creative Commons Attribution

@contact:    pascal@pascalvaneck.com
@deffield    updated: Updated
'''

import sys
import os
import urllib.request
import logging
import threading
import time
import functools
import operator
import socket
import collections
import re

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

__all__ = []
__version__ = 0.1
__date__ = '2013-08-11'
__updated__ = '2013-08-11'

DEBUG = 0
TESTRUN = 0
PROFILE = 0
LOGGER = logging.getLogger(__name__)
STATIC_RESULTS = []
SSE_RESULTS = []
OVERALL_SIZE = []

class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''

    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg

    def __str__(self):
        return self.msg

    def __unicode__(self):
        return self.msg


def main(argv=None):  # IGNORE:C0111
    '''Command line options.'''

    global DEBUG

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

  Created by Pascal van Eck on %s.
  Copyright 2013 organization_name. All rights reserved.

  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license,
                                formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-v", "--verbose", action="store_true",
                            help="set verbosity level [default: %(default)s]")
        parser.add_argument("-d", "--debug", action="store_true",
                            help="produce debug output")
        parser.add_argument("-V", "--version", action="version",
                            version=program_version_message)
        parser.add_argument("-p", "--port", type=int, default=7737,
                            metavar="N", help="set port to listen on "
                            "[default: %(default)s]")
        parser.add_argument("-l", "--load", type=int, default=10,
                            metavar="N", help="number of times to load site "
                            "[default: %(default)s]")
        parser.add_argument("-w", "--wait", type=int, default=100,
                            metavar="N", help="waiting time (ms) between loads "
                            "[default: %(default)s]")
        parser.add_argument("url", metavar="url", nargs="?",
                            default="http://localhost:7737",
                            help="URL to load [default: %(default)s]")

        # Process arguments
        args = parser.parse_args()

        verbose = args.verbose
        DEBUG = args.debug  # pylint: disable=W0603
        url = args.url
        waiting_time = args.wait
        load = args.load

        if verbose > 0:
            logging.basicConfig(level=logging.INFO)

        if DEBUG > 0:
            logging.basicConfig(level=logging.DEBUG)

        LOGGER.info("sseserver.py: Verbosity level %s.", verbose)
        LOGGER.info("loadsimulator: starting main loop.")
        subthreads = []
        start_time = time.time()
        for count in range(0, load):
            site_loader = SiteLoader(url, threading.current_thread())
            site_loader.start()
            subthreads.append(site_loader)
            time.sleep(waiting_time / 1000)
        for thread in subthreads:
            thread.join()
        end_time = time.time()
        time_passed = end_time - start_time
        LOGGER.info("loadsimulator: ending main loop.")
        grand_total = functools.reduce(operator.add, map(int, OVERALL_SIZE))
        LOGGER.info("loadsimulator: %s bytes loaded in %s seconds (%s kB/s).",
                    grand_total, time_passed, (grand_total / 1024) / time_passed)
        LOGGER.info("loadsimulator: static results = %s", STATIC_RESULTS)
        LOGGER.info("loadsimulator: SSE results = %s", SSE_RESULTS)

        return 0
    except KeyboardInterrupt:
        sys.exit()
        return 0
    except Exception as ex:
        if DEBUG or TESTRUN:
            raise(ex)
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(ex) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2

STATIC_RESOURCES = ["", "css/960.css", "css/dashboard.css", "css/jasmine.css",
                    "js/gadget.js", "js/handlers.js", "js/main.js",
                    "js/view.js", "js/requirejs-config.js", "js/tweetboard.js",
                    "js/highcharts_uttheme.js", "lib/js/highcharts.js",
                    "lib/js/jasmine.js", "lib/js/jasmine-html.js",
                    "lib/js/jquery-1.8.2.min.js", "lib/js/require.js"]


class SiteLoader(threading.Thread):

    def __init__(self, base_url, parent):
        threading.Thread.__init__(self)
        self._base_url = base_url
        self.lengths = []
        self.results = []
        self._parent = parent

    def run(self):
        LOGGER.info("loadsimulator: starting to load %s.", self._base_url)
        start_time = time.time()

        # 1. Load all static resources concurrently (like a browser would):
        subthreads = []
        for static_resource in STATIC_RESOURCES:
            url = self._base_url + "/" + static_resource
            url_loader = URLloader(url, threading.current_thread())
            url_loader.start()
            subthreads.append(url_loader)
        for thread in subthreads:
            thread.join()
        end_time = time.time()
        time_passed = end_time - start_time
        total_size = functools.reduce(operator.add, map(int, self.lengths))
        OVERALL_SIZE.append(total_size)
        LOGGER.info("loadsimulator: %s bytes loaded in %s seconds (%s kB/s).",
                    total_size, time_passed, (total_size / 1024) / time_passed)
        if len(self.results) != len(STATIC_RESOURCES):
            LOGGER.warning("loadsimulator: not all URLloaders reported "
                           "success.")
        static_results_counter = collections.Counter(self.results)
        STATIC_RESULTS.append(static_results_counter)
        LOGGER.info("loadsimulator: %s.", static_results_counter)

        # 2. Start loading events using the SSE protocol
        try:
            re_url = r"^(?:(https?)://)?((?:[\w]+\.)*[\w]+)(?::([0-9]+))?(\S*)"
            url_parts = re.split(re_url, url)
            if url_parts[3] == None:
                url_parts[3] = 80
            events = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            events.connect((url_parts[2], int(url_parts[3])))
            events.sendall(b"GET /events HTTP/1.1\r\nCache-Control: no-cache\r\n"
                           b"Accept: text/event-stream\r\n\r\n")
            if receive_headers(events) == "200":
                messages_received = 0
                expected_ident = None
                stop = False
                while not stop:
                    ident, eventtype, message_data = receive_sse_message(events)
                    messages_received += 1
                    LOGGER.debug("loadsimulator: received message %s: ID=%s, "
                                 "type=%s, data=%s.", messages_received,
                                                        ident, eventtype,
                                                        message_data)
                    if (expected_ident != None) and (expected_ident != ident):
                        LOGGER.warning("loadsimulator: missing message.")
                        SSE_RESULTS.append("Missing")
                    if messages_received > 10:
                        stop = True
                    expected_ident = ident + 1
                SSE_RESULTS.append("OK")
            else:
                LOGGER.warning("loadsimulator: cannot connect to eventsource.")
                SSE_RESULTS.append("noconnection")
        except ConnectionResetError:
            SSE_RESULTS.append("exception")
        except:
            LOGGER.warning("loadsimulator: detected error while listening to "
                           "events.")
            SSE_RESULTS.append("exception")
        finally:
            events.close()


class URLloader(threading.Thread):

    def __init__(self, url, parent):
        threading.Thread.__init__(self)
        self._url = url
        self._parent = parent

    def run(self):
        try:
            response = urllib.request.urlopen(self._url)
            LOGGER.debug("loadsimulator: loaded %s (status: %s).", self._url,
                        response.status)
            self._parent.lengths.append(response.getheader("Content-Length", 0))
            contents = response.read()
            if len(contents) != int(response.getheader("Content-Length", 0)):
                LOGGER.warning("loadsimulator: seems we got an incomplete "
                               "response")
            self._parent.results.append(response.status)
        except urllib.error.HTTPError as ex:
            LOGGER.warning("HTTPError getting %s: %s (%s).", self._url, ex.code,
                           ex.reason)
            self._parent.results.append("exception")
        except urllib.error.URLError as ex:
            LOGGER.warning("URLError getting %s: %s.", self._url, ex.reason)
            self._parent.results.append("exception")
        except:
            LOGGER.warning("Exception getting %s.", self._url)
            self._parent.results.append("exception")


def receive_headers(eventsocket):
    end_of_headers = False
    while not end_of_headers:
        data = eventsocket.recv(4096).decode("utf-8")
        match = re.search(r"^HTTP/[0-9]\.[0-9] ([0-9]+) ([A-Z]+)\r\n", data)
        if match:
            status = match.group(1)
        match = re.search(r"\r\n\r\n", data)
        if match:
            end_of_headers = True
    return status


def receive_sse_message(eventsocket):
    end_of_message = False
    while not end_of_message:
        data = eventsocket.recv(4096).decode("utf-8")
        match = re.search(r"id: ([0-9]+)\r\n", data)
        if match:
            ident = int(match.group(1))
        match = re.search(r"event: (\S+)\r\n", data)
        if match:
            eventtype = match.group(1)
        match = re.search(r"data: (.*)\r\n", data)
        if match:
            message_data = match.group(1)
        match = re.search(r"\r\n\r\n", data)
        if match:
            end_of_message = True
    return (ident, eventtype, message_data)


if __name__ == "__main__":
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = 'tests.integration.loadsimulator_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())
