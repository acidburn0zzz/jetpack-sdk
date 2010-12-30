
import os
import unittest
from cuddlefish.apiparser import parse_hunks, ParseError
from cuddlefish.apirenderer import md_to_html

tests_path = os.path.abspath(os.path.dirname(__file__))
static_files_path = os.path.join(tests_path, "static-files")

class ParserTests(unittest.TestCase):
    def pathname(self, filename):
        return os.path.join(static_files_path, "docs", filename)

    def render_markdown(self, pathname):
        return self.md_to_html(pathname)

    def test_renderer(self):
        html = self.parse(self.pathname("APIsample.md"))
        reference = open(self.pathname("APIreference.html")).read()
        self.assertEqual(html, reference)
       
if __name__ == "__main__":
    unittest.main()
