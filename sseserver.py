#!/usr/local/bin/python2.7
# encoding: utf-8
'''
sseserver -- Python script that serves server-sent events

sseserver is a description

@author:     Pascal van Eck

@copyright:  2013 University of Twente. All rights reserved.

@license:    license

@contact:    p.vaneck@utwente.nl
@deffield    updated: May 31, 2013
'''

import sys
import os
import SseHTTPServer
import SocketServer
import logging
import Queue

from argparse import ArgumentParser, FileType
from argparse import RawDescriptionHelpFormatter

__all__ = []
__version__ = 0.1
__date__ = '2013-05-31'
__updated__ = '2013-05-31'

DEBUG = 1
TESTRUN = 0
PROFILE = 0

class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg


def myQueue():
    return [
            {"data": ["Line 1 of first message.", "Line 2 of first message."]},
            {"data": ["Line 1 of second message.", "Line 2 of second message."]}
            ]

def main(argv=None):
    '''Command line options.'''

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

  Created by user_name on %s.
  Copyright 2013 organization_name. All rights reserved.

  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-v", "--verbose", action="count", help="set verbosity level [default: %(default)s]")
        parser.add_argument("-V", "--version", action="version", version=program_version_message)
        parser.add_argument("-p", "--port", type=int, default=7737, metavar="N", help="set port to listen on [default: %(default)s]")
        parser.add_argument("infile", nargs="?", type=FileType("r"), default=sys.stdin, help="file containing event messages [default: %(default)s]")

        # Process arguments
        args = parser.parse_args()

        verbose = args.verbose
        port = args.port
        infile = args.infile

        logging.info("Verbosity level %s.", verbose)

        if verbose > 0:
            logging.info("sseserver.py: Serving contents of %s via port %s.", infile.name, port)

        for message in myQueue():
            SseHTTPServer.SseHTTPRequestHandler.event_queue.put(message)

        Handler = SseHTTPServer.SseHTTPRequestHandler
        httpd = SocketServer.ThreadingTCPServer(("127.0.0.1", port), Handler)
        httpd.serve_forever()

        return 0
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception, e:
        if DEBUG or TESTRUN:
            raise(e)
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2

if __name__ == "__main__":
    if DEBUG:
        logging.basicConfig(level=logging.DEBUG)
        sys.argv.append("-v")
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = 'sseserver_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())
