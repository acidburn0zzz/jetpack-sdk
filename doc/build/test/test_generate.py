# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import shutil
import unittest
import StringIO
import tarfile
import HTMLParser
import urlparse
import urllib

from build import generate

INITIAL_FILESET = [ ["static-files", "base.html"], \
                    ["dev-guide", "index.html"], \
                    ["modules", "sdk", "aardvark-feeder.html"], \
                    ["modules", "sdk", "anteater", "anteater.html"], \
                    ["modules", "packages", "third_party.html"]]

EXTENDED_FILESET = [ ["static-files", "base.html"], \
                    ["dev-guide", "extra.html"], \
                    ["dev-guide", "index.html"], \
                    ["modules", "sdk", "aardvark-feeder.html"], \
                    ["modules", "sdk", "anteater", "anteater.html"],\
                    ["modules", "packages", "third_party.html"]]

EXTRAFILE = ["dev-guide", "extra.html"]

def env_root(): 
    this_directory = os.path.dirname(__file__)
    this_directory_pieces = this_directory.split(os.sep)
    # this_directory is root + "doc" + "build" + "test"
    return os.sep.join(this_directory_pieces[:-3])

def get_test_root():
    return os.path.join(env_root(), "python-lib", "cuddlefish", "tests", "static-files")

def get_sdk_docs_root():
    return os.path.join(get_test_root(), "sdk-docs")

def get_base_url_path():
    return os.path.join(get_sdk_docs_root(), "doc")

def url_from_path(path):
    path = path.lstrip("/")
    return "file://"+"/"+"/".join(path.split(os.sep))+"/"

def get_base_url():
    return url_from_path(get_base_url_path())

class Link_Checker(HTMLParser.HTMLParser):
    def __init__(self, tester, filename, base_url):
        HTMLParser.HTMLParser.__init__(self)
        self.tester = tester
        self.filename = filename
        self.base_url = base_url
        self.errors = []

    def handle_starttag(self, tag, attrs):
        link = self.find_link(attrs)
        if link:
            self.validate_link(link)

    def handle_startendtag(self, tag, attrs):
        link = self.find_link(attrs)
        if link:
            self.validate_link(link)

    def find_link(self, attrs):
        attrs = dict(attrs)
        href = attrs.get('href', '')
        if href:
            parsed = urlparse.urlparse(href)
            if not parsed.scheme:
                return href
        src = attrs.get('src', '')
        if src:
            parsed = urlparse.urlparse(src)
            if not parsed.scheme:
                return src

    def validate_link(self, link):
        parsed = urlparse.urlparse(link)
        # there should not be any file:// URLs
        self.tester.assertNotEqual(parsed.scheme, "file")
        # any other absolute URLs will not be checked
        if parsed.scheme:
            return
        current_path_as_url = url_from_path(os.path.dirname(self.filename))
        # otherwise try to open the file at: baseurl + path
        absolute_url = current_path_as_url + parsed.path
        try:
            urllib.urlopen(absolute_url)
        except IOError:
            self.errors.append(self.filename + "\n    " + absolute_url)

class Generate_Docs_Tests(unittest.TestCase):

    def test_generate_static_docs(self):

        def cleanup():
            shutil.rmtree(get_base_url_path())
            generate.clean_generated_docs(os.path.join(env_root(), "doc"))

        # make sure we start clean
        if os.path.exists(get_base_url_path()):
            shutil.rmtree(get_base_url_path())
        base_url = get_base_url()
        broken_links = []
        # get each HTML file...
        for root, subFolders, filenames in os.walk(get_sdk_docs_root()):
            for filename in filenames:
                if not filename.endswith(".html"):
                    continue
                if root.endswith("static-files"):
                    continue
                filename = os.path.join(root, filename)
                # ...and feed it to the link checker
                linkChecker = Link_Checker(self, filename, base_url)
                linkChecker.feed(open(filename, "r").read())
                broken_links.extend(linkChecker.errors)
        if broken_links:
            print
            print "The following links are broken:"
            for broken_link in sorted(broken_links):
                print " "+ broken_link

            cleanup()
            self.fail("%d links are broken" % len(broken_links))

        cleanup()

if __name__ == '__main__':
    unittest.main()
