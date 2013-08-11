#!/usr/bin/env python3
# encoding: utf-8
u'''
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
import tweetprocessor
import logging
from argparse import ArgumentParser, FileType
from argparse import RawDescriptionHelpFormatter
from io import open

__all__ = []
__version__ = 0.1
__date__ = u'2013-05-31'
__updated__ = u'2013-05-31'

DEBUG = 0
TESTRUN = 0
PROFILE = 0


class CLIError(Exception):
    u'''Generic exception to raise and log different fatal errors.'''

    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = u"E: %s" % msg

    def __str__(self):
        return self.msg

    def __unicode__(self):
        return self.msg


def main(argv=None):
    u'''Command line options.'''

    global DEBUG

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = u"v%s" % __version__
    program_build_date = unicode(__updated__)
    program_version_message = u'%%(prog)s %s (%s)' % (program_version,
                                                     program_build_date)
    program_shortdesc = __import__(u'__main__').__doc__.split(u"\n")[1]
    program_license = u'''%s

  Created by user_name on %s.
  Copyright 2013 organization_name. All rights reserved.

  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, unicode(__date__))

    verbose = False
    DEBUG = False

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license,
                                formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument(u"-v", u"--verbose", action=u"store_true",
                            help=u"set verbosity level [default: %(default)s]")
        parser.add_argument(u"-d", u"--debug", action=u"store_true",
                            help=u"produce debug output")
        parser.add_argument(u"-V", u"--version", action=u"version",
                            version=program_version_message)
        parser.add_argument(u"-p", u"--port", type=int, default=7737,
                            metavar=u"N", help=u"set port to listen on "
                            u"[default: %(default)s]")
        parser.add_argument(u"infile", nargs=u"?", type=FileType(u"r"),
                            default=sys.stdin, help=u"file containing event "
                            u"messages [default: %(default)s]")

        # Process arguments
        args = parser.parse_args()

        verbose = args.verbose
        DEBUG = args.debug  # pylint: disable=W0603
        port = args.port
        infile = args.infile

        if verbose > 0:
            logging.basicConfig(level=logging.INFO)

        if DEBUG > 0:
            logging.basicConfig(level=logging.DEBUG)

        logging.info(u"sseserver.py: Verbosity level %s.", verbose)
        logging.info(u"sseserver.py: Serving contents of %s via port %s.",
                     infile.name, port)

        tweetprocessor.process_tweets(infile, port)

        return 0
    except KeyboardInterrupt:
        sys.exit()
        return 0
    except Exception, ex:
        if DEBUG or TESTRUN:
            raise(ex)
        indent = len(program_name) * u" "
        sys.stderr.write(program_name + u": " + repr(ex) + u"\n")
        sys.stderr.write(indent + u"  for help use --help")
        return 2

if __name__ == u"__main__":
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        PROFILE_FILENAME = u'sseserver_profile.txt'
        cProfile.run(u'main()', PROFILE_FILENAME)
        STATSFILE = open(u"profile_stats.txt", u"wb")
        P = pstats.Stats(PROFILE_FILENAME, stream=STATSFILE)
        STATS = P.strip_dirs().sort_stats(u'cumulative')
        STATS.print_stats()
        STATSFILE.close()
        sys.exit(0)
    sys.exit(main())
