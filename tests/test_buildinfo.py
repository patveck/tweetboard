'''
Created on 26 jul. 2013

@author: patveck
'''
import unittest
from unittest.mock import patch
import buildinfo
import platform
import io


def side_effect_windows_success(path):
    if path == "C:\\Users\\user\\tweetboard\\p1\\p2\\.git":
        return False
    if path == "C:\\Users\\user\\tweetboard\\p1\\.git":
        return False
    if path == "C:\\Users\\user\\tweetboard\\.git":
        return True
    raise ValueError


def side_effect_success(path):
    if platform.system() == "Windows":
        return side_effect_windows_success(path)
    else:
        if path == "/home/user/tweetboard/p1/p2/.git":
            return False
        if path == "/home/usr/tweetboard/p1/.git":
            return False
        if path == "/home/usr/tweetboard/.git":
            return True
        raise ValueError


def side_effect_windows_notfound(path):
    if path == "C:\\Users\\user\\tweetboard\\p1\\p2\\.git":
        return False
    if path == "C:\\Users\\user\\tweetboard\\p1\\.git":
        return False
    if path == "C:\\Users\\user\\tweetboard\\.git":
        return False
    if path == "C:\\Users\\user\\.git":
        return False
    if path == "C:\\Users\\.git":
        return False
    if path == "C:\\.git":
        return False
    raise ValueError


def side_effect_notfound(path):
    if platform.system() == "Windows":
        return side_effect_windows_notfound(path)
    else:
        if path == "/home/user/tweetboard/p1/p2/.git":
            return False
        if path == "/home/usr/tweetboard/p1/.git":
            return False
        if path == "/home/usr/tweetboard/.git":
            return False
        if path == "/home/usr/.git":
            return False
        if path == "/home/.git":
            return False
        if path == "/.git":
            return False
        raise ValueError


class Test(unittest.TestCase):

    def test_is_valid(self):
        self.assertTrue(buildinfo.
                    is_valid_sha("bc1850f08773f2b7bbe13d69f6f3f0b9d64c8402"),
                    "This SHA should be valid.")
        self.assertFalse(buildinfo.is_valid_sha(""),
                         "Empty string is not a valid SHA.")
        self.assertFalse(buildinfo.is_valid_sha("bc1850f08"),
                         "This string is too short to be a valid SHA.")

    def test_get_git_directory_root(self):
        self.assertRaises(IOError, buildinfo.get_git_directory, "/")
        self.assertRaises(IOError, buildinfo.get_git_directory, "C:\\")

    def test_get_git_directory_success(self):
        with patch("os.path.exists") as mock:
            mock.side_effect = side_effect_success
            if platform.system() == "Windows":
                path = "C:\\Users\\user\\tweetboard\\p1\\p2\\m.py"
                git = "C:\\Users\\user\\tweetboard\\.git"
            else:
                path = "/home/user/tweetboard/p1/p2/m.py"
                git = "/home/user/tweetboard/.git"
            self.assertEqual(buildinfo.get_git_directory(path), git,
                             "Wrong .git directory")

    def test_get_git_directory_notfound(self):
        with patch("os.path.exists") as mock:
            mock.side_effect = side_effect_notfound
            if platform.system() == "Windows":
                path = "C:\\Users\\user\\tweetboard\\p1\\p2\\m.py"
            else:
                path = "/home/user/tweetboard/p1/p2/m.py"
            self.assertRaises(IOError, buildinfo.get_git_directory, path)

    def test_load_sha_success(self):
        sha = "bc1850f08773f2b7bbe13d69f6f3f0b9d64c8402"
        pseudofile = io.StringIO(sha + "\n")
        head_line = "ref: refs/heads/feature/newfeat"
        with patch("builtins.open", return_value=pseudofile):
            with patch("os.path.exists", return_value=True):
                gitinfo = buildinfo.load_sha("/home/usr/.git", head_line)
                self.assertEqual(gitinfo, {"branch": "feature/newfeat",
                                           "commit": sha},
                                 "Should return correct gitinfo")

    def test_load_sha_failure(self):
        sha = "bc1850f08773f2b7bbe13d69f6f3f0b9d64c8402"
        pseudofile = io.StringIO(sha + "\n")
        head_line = "ref: refs/heads/feature/newfeat"
        with patch("builtins.open", return_value=pseudofile):
            with patch("os.path.exists", return_value=False):
                gitinfo = buildinfo.load_sha("/home/usr/.git", head_line)
                self.assertEqual(gitinfo, {"branch": "feature/newfeat",
                                           "commit": "SHANotFound"},
                                 "Should return correct gitinfo")

    def test_get_buildinfo_detached(self):
        sha = "bc1850f08773f2b7bbe13d69f6f3f0b9d64c8402"
        pseudofile = io.StringIO(sha + "\n")
        with patch("builtins.open", return_value=pseudofile):
            with patch("buildinfo.get_git_directory",
                       return_value="/home/user.git"):
                gitinfo = buildinfo.get_buildinfo("/home/usr/foo.py")
                self.assertEqual(gitinfo, {"branch": "detached",
                                           "commit": sha},
                                 "Should return (detached, sha).")

    def test_get_buildinfo_branch(self):
        sha = "bc1850f08773f2b7bbe13d69f6f3f0b9d64c8402"
        pseudofile = io.StringIO("ref: refs/heads/feature/newfeat\n")
        with patch("builtins.open", return_value=pseudofile):
            with patch("buildinfo.get_git_directory",
                       return_value="/home/user.git"):
                with patch("buildinfo.load_sha",
                           return_value={"branch": "feature/newfeat",
                                         "commit": sha}):
                    gitinfo = buildinfo.get_buildinfo("/home/usr/foo.py")
                    self.assertEqual(gitinfo, {"branch": "feature/newfeat",
                                               "commit": sha},
                                     "Should return (feature/newfeat, sha).")


if __name__ == "__main__":
    unittest.main()
