
import os
import unittest

from cuddlefish import apiparser
from cuddlefish import apirenderer
from cuddlefish import docstract

tests_path = os.path.abspath(os.path.dirname(__file__))
static_files_path = os.path.join(tests_path, "static-files")

class ParserTests(unittest.TestCase):

    def render_markdown(self, pathname):
        return md_to_html(pathname)
        md_path = os.path.join(static_files_path, "docs", "APIsample.md")
        module_json_md = apiparser_md.get_api_json(open(md_path).read())
        module_div_md = apirenderer.json_to_div(module_json_md, "APIsample")

    def test_renderer(self):
        test = self.render_markdown(self.pathname("APIsample.md"))
        reference = open(self.pathname("APIreference.html")).read()
        test_lines = test.splitlines(True)
        reference_lines = reference.splitlines(True)
        for x in range(len(test_lines)):
            self.assertEqual(test_lines[x], reference_lines[x])

if __name__ == "__main__":
    unittest.main()
