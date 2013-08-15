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
import sseclient

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
        for count in range(0, load):
            site_loader = SiteLoader(url)
            site_loader.start()
            subthreads.append(site_loader)
            time.sleep(waiting_time / 1000)
        for thread in subthreads:
            thread.join()
        LOGGER.info("loadsimulator: ending main loop.")

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

    def __init__(self, base_url):
        threading.Thread.__init__(self)
        self._base_url = base_url
        self.lengths = []

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
        LOGGER.info("loadsimulator: %s bytes loaded in %s seconds (%s kB/s).",
                    total_size, time_passed, (total_size / 1024) / time_passed)

        # 2. Start loading events using the SSE protocol
        try:
            messages = sseclient.SSEClient(self._base_url + "/events")
            for msg in messages:
                LOGGER.debug("loadsimulator: received message %s.", msg)
        except ConnectionResetError:
            pass
        except:
            LOGGER.warning("loadsimulator: detected error while listening to "
                           "events.")


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
            # contents = response.read()
            # if len(contents) != int(response.getheader("Content-Length", 0)):
            #    LOGGER.warning("loadsimulator: seems we got an incomplete "
            #                   "response")
        except urllib.error.HTTPError as ex:
            LOGGER.warning("HTTPError getting %s: %s (%s).", self._url, ex.code,
                           ex.reason)
        except urllib.error.URLError as ex:
            LOGGER.warning("URLError getting %s: %s.", self._url, ex.reason)


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
