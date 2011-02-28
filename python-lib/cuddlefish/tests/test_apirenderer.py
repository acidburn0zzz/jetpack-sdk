
import os
import unittest

from cuddlefish import apiparser_md
from cuddlefish import apirenderer
from cuddlefish import docstract

test_files_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static-files", "docs")

class ParserTests(unittest.TestCase):

    def render_markdown(self):
        md_path = os.path.join(test_files_path, "APIsample.md")
        module_json_md = apiparser_md.parse_api_doc(open(md_path).read())
        module_html_md = apirenderer.json_to_html(module_json_md, "APIsample")
        return module_html_md

    def test_renderer(self):
        test = self.render_markdown()
        reference = open(os.path.join(test_files_path, "APIreference.html")).read()
        test_lines = test.splitlines(True)
        reference_lines = reference.splitlines(True)
        for x in range(len(test_lines)):
            self.assertEqual(test_lines[x], reference_lines[x])

if __name__ == "__main__":
    unittest.main()
