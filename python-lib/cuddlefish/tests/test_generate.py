import os
import shutil
import unittest
import StringIO
import tarfile
import HTMLParser

from cuddlefish.docs import generate
from cuddlefish.tests import env_root

INITIAL_FILESET = [ ["static-files", "base.html"], \
                    ["dev-guide", "welcome.html"], \
                    ["packages", "aardvark", "aardvark.html"] ]

EXTENDED_FILESET = [ ["static-files", "base.html"], \
                    ["dev-guide", "extra.html"], \
                    ["dev-guide", "welcome.html"], \
                    ["packages", "aardvark", "aardvark.html"] ]

EXTRAFILE = ["dev-guide", "extra.html"]

BASE_URL = []

class Link_Checker(HTMLParser.HTMLParser):
    def __init__(self, tester):
        HTMLParser.HTMLParser.__init__(self)
        self.tester = tester

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            href = dict(attrs).get('href', '')
            if href:
                self.validate_href(href)

    def validate_href(self, href):
        self.tester.assertFalse(href.startswith("file"))

class Generate_Docs_Tests(unittest.TestCase):
    def test_root(self):
        return os.path.join(env_root, "python-lib", "cuddlefish", "tests", "static-files")

    def sdk_docs_root(self):
        return os.path.join(self.test_root(), "sdk-docs")

    def base_url_path(self):
        return os.path.join(self.sdk_docs_root(), "doc")

    def base_url(self):
        base_url_path = self.base_url_path()
        # this is to ensure the path starts with "/"
        # whether or not it's on Windows
        # there might be a better way
        if not base_url_path.startswith("/"):
            base_url_path = "/" + base_url_path
        base_url_path_pieces = base_url_path.split(os.sep)
        base_url = "file://" + "/".join(base_url_path_pieces) + "/"
        return base_url

    def test_generate_static_docs_does_not_smoke(self):
        # make sure we start clean
        filename = 'testdocs.tgz'
        if os.path.exists(filename):
            os.remove(filename)
        if os.path.exists(self.base_url_path()):
            shutil.rmtree(self.base_url_path())
        # generate a doc tarball, and extract it
        filename = generate.generate_static_docs(env_root, self.base_url())
        tgz = tarfile.open(filename)
        tgz.extractall(self.sdk_docs_root())
        # look in each HTML file

        for root, subFolders, filenames in os.walk(self.sdk_docs_root()):
            for filename in filenames:
                if not filename.endswith(".html"):
                    continue
         #       print os.path.join(root, filename)
                # we'll create this for each file, so that if there's an error
                # we get a usable line number
                linkChecker = Link_Checker(self)
                linkChecker.feed(open(os.path.join(root, filename), "r").read())

   #     self.assertTrue(os.path.exists(filename))
   #     os.remove(filename)
        shutil.rmtree(self.base_url_path())

    def test_generate_docs_does_not_smoke(self):
        test_root = self.test_root()
        docs_root = os.path.join(test_root, "doc")
        generate.clean_generated_docs(docs_root)
        new_digest = self.check_generate_regenerate_cycle(test_root, INITIAL_FILESET)
        # touching an MD file under packages **does** cause a regenerate
        os.utime(os.path.join(test_root, "packages", "aardvark", "doc", "main.md"), None)
        new_digest = self.check_generate_regenerate_cycle(test_root, INITIAL_FILESET, new_digest)
        # touching a non MD file under packages **does not** cause a regenerate
        os.utime(os.path.join(test_root, "packages", "aardvark", "lib", "main.js"), None)
        self.check_generate_is_skipped(test_root, INITIAL_FILESET, new_digest)
        # touching a non MD file under static-files **does not** cause a regenerate
        os.utime(os.path.join(docs_root, "static-files", "base.html"), None)
        new_digest = self.check_generate_is_skipped(test_root, INITIAL_FILESET, new_digest)
        # touching an MD file under dev-guide **does** cause a regenerate
        os.utime(os.path.join(docs_root, "dev-guide-source", "welcome.md"), None)
        new_digest = self.check_generate_regenerate_cycle(test_root, INITIAL_FILESET, new_digest)
        # adding a file **does** cause a regenerate
        open(os.path.join(docs_root, "dev-guide-source", "extra.md"), "w").write("some content")
        new_digest = self.check_generate_regenerate_cycle(test_root, EXTENDED_FILESET, new_digest)
        # deleting a file **does** cause a regenerate
        os.remove(os.path.join(docs_root, "dev-guide-source", "extra.md"))
        new_digest = self.check_generate_regenerate_cycle(test_root, INITIAL_FILESET, new_digest)
        # remove the files
        generate.clean_generated_docs(docs_root)

    def check_generate_is_skipped(self, test_root, files_to_expect, initial_digest):
        generate.generate_docs(test_root, stdout=StringIO.StringIO())
        docs_root = os.path.join(test_root, "doc")
        for file_to_expect in files_to_expect:
            self.assertTrue(os.path.exists(os.path.join(docs_root, *file_to_expect)))
        self.assertTrue(initial_digest == open(os.path.join(docs_root, "status.md5"), "r").read())

    def check_generate_regenerate_cycle(self, test_root, files_to_expect, initial_digest = None):
        # test that if we generate, files are getting generated
        generate.generate_docs(test_root, stdout=StringIO.StringIO())
        docs_root = os.path.join(test_root, "doc")
        for file_to_expect in files_to_expect:
            self.assertTrue(os.path.exists(os.path.join(docs_root, *file_to_expect)))
        if initial_digest:
            self.assertTrue(initial_digest != open(os.path.join(docs_root, "status.md5"), "r").read())
        # and that if we regenerate, nothing changes...
        new_digest = open(os.path.join(docs_root, "status.md5"), "r").read()
        self.check_generate_is_skipped(test_root, files_to_expect, new_digest)
        return new_digest

if __name__ == '__main__':
    unittest.main()
