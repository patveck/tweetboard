u'''
Created on 26 jul. 2013

Inspired by
https://github.com/adobe/brackets/blob/master/src/utils/BuildInfoUtils.js

@author: patveck
'''

import re
import os.path
from io import open


def is_valid_sha(sha):
    u'''Test whether sha is a valid SHA, which currently means that it is a
    string of exactly 40 characters from the range a-f and 0-9.'''
    _match = re.match(ur"[0-9a-f]{40}", sha)
    if _match:
        return True
    else:
        return False


def get_git_directory(path):
    u'''Determine where the .git directory is relative to path, if it exists in
    the first place. Do so recursively:
    - If we are at the root, raise an IOError to signal that the .git
      directory has not been found
    - If .git exists in path, return path/.git
    - Otherwise, recurse by calling this function on path/.. (the parent dir)'''
    (_head, _tail) = os.path.split(os.path.realpath(path))
    if _tail == u"" and (_head == u"/" or _head[2:] == u"\\"):
        raise IOError
    else:
        _candidate = os.path.join(_head, u".git")
        if os.path.exists(_candidate):
            return os.path.abspath(_candidate)
        else:
            return get_git_directory(os.path.join(path, u".."))


def load_sha(basepath, head_line):
    u'''Handle case where .git/HEAD contains a pointer to a file containing the
    SHA of the commit. Determine the name of this file, read the first line of
    it, which should be a valid SHA.'''
    _ref_rel_path = head_line[5:]
    _branch = head_line[16:]
    _path = os.path.join(basepath, _ref_rel_path)
    if os.path.exists(_path):
        try:
            _line = open(_path, u"r").readline().strip()
        except IOError:
            return ({u"branch": _branch, u"commit": u"SHANotFound"})
        if is_valid_sha(_line):
            return ({u"branch": _branch, u"commit": _line})
        else:
            return ({u"branch": _branch, u"commit": u"InvalidSHA"})
    else:
        return ({u"branch": _branch, u"commit": u"SHANotFound"})


def get_buildinfo(path):
    u'''Tries to get Git branch name and SHA of working directory. Always
    returns a tuple (branch, sha) with two non-empty strings, never raises
    an exception.'''

    # Read first line from file .git/HEAD, find out where .git is first:
    try:
        _git_directory = get_git_directory(path)
        _line = open(os.path.join(_git_directory, u"HEAD"),
                     u"r").readline().strip()
    except IOError:
        return ({u"branch": u"BranchNotFound", u"commit": u"SHANotFound"})

    # _line now contains the first line of .git/HEAD. This either contains
    # a valid SHA1 in the case of a so-called detached head, or it contains
    # a pointer to another file that contains the SHA
    if is_valid_sha(_line):
        return ({u"branch": u"detached", u"commit": _line})
    elif _line.startswith(u"ref: "):
        return load_sha(_git_directory, _line)
    else:
        return ({u"branch": u"BranchNotFound", u"commit": u"SHANotFound"})


def test(path=__file__):
    u'''Test main functionality simply by calling it on a path'''
    print get_buildinfo(path)

if __name__ == u'__main__':
    print u"buildinfo.py: calling test(%s)" % __file__
    test(__file__)
