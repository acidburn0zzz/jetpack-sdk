
import os, shutil
import unittest
from cuddlefish import apiparser
from cuddlefish import apiparser_md
from cuddlefish import apirenderer
from cuddlefish import docstract

tests_path = os.path.abspath(os.path.dirname(__file__))
static_files_path = os.path.join(tests_path, "static-files")

md_desc = "Markdown description\n"
md_api = "Markdown-documented function"
js_desc = "JavaScript description"
js_api = "JavaScript-documented function"

class ParserTests(unittest.TestCase):
    def package_path(self):
        return os.path.join(static_files_path, "packages", "aardvark")

    def sample_path(self):
        return os.path.join(static_files_path, "docs")

    def test_md_path(self):
        return os.path.join(static_files_path, "packages", "aardvark", "docs")

    def test_js_path(self):
        return os.path.join(static_files_path, "packages", "aardvark", "lib")

    def _test_result(self, desc_function, api_function):
        module_json = apiparser.get_api_json(self.package_path(), "test")
        desc_function(module_json)
        api_function(module_json)

# this table defines the rules for combining docs found in Markdown files
# with docs found in JS files
#
# MD or JS files can contain:
# - both description and API reference
# - either description or API reference
# - neither
# Additionally MD files can be nonexistent.
# 
# Each cell in the table represents the source of the description and the API
# reference, respectively.
#
#    MD |  all  |  desc  | API  | empty | nonexistent
#  JS  ----------------------------------------------
#  all  | MD-MD | MD-JS  | --MD | --JS  | JS-JS
#  desc | MD-MD | MD--   | --MD | ----  | JS--
#  API  | MD-MD | MD-JS  | --MD | --JS  | --JS
# empty | MD-MD | MD--   | --MD | ----  | ----
#
    def test_apiparser_md_or_js(self):
        # JS has desc and API, iterate through MD permutations
        shutil.copyfile(os.path.join(self.test_md_path(), "all.md"), os.path.join(self.test_md_path(), "test.md"))
        shutil.copyfile(os.path.join(self.test_js_path(), "all.js"), os.path.join(self.test_js_path(), "test.js"))
        self._test_result(self.MD_desc, self.MD_API)

        shutil.copyfile(os.path.join(self.test_md_path(), "desc.md"), os.path.join(self.test_md_path(), "test.md"))
        self._test_result(self.MD_desc, self.JS_API)

        shutil.copyfile(os.path.join(self.test_md_path(), "api.md"), os.path.join(self.test_md_path(), "test.md"))
        self._test_result(self.empty_desc, self.MD_API)

        shutil.copyfile(os.path.join(self.test_md_path(), "empty.md"), os.path.join(self.test_md_path(), "test.md"))
        self._test_result(self.empty_desc, self.JS_API)

        os.remove(os.path.join(self.test_md_path(), "test.md"))
        self._test_result(self.JS_desc, self.JS_API)

        # JS has desc only, iterate through MD permutations
        shutil.copyfile(os.path.join(self.test_md_path(), "all.md"), os.path.join(self.test_md_path(), "test.md"))
        shutil.copyfile(os.path.join(self.test_js_path(), "desc.js"), os.path.join(self.test_js_path(), "test.js"))
        self._test_result(self.MD_desc, self.MD_API)

        shutil.copyfile(os.path.join(self.test_md_path(), "desc.md"), os.path.join(self.test_md_path(), "test.md"))
        self._test_result(self.MD_desc, self.empty_API)

        shutil.copyfile(os.path.join(self.test_md_path(), "api.md"), os.path.join(self.test_md_path(), "test.md"))
        self._test_result(self.empty_desc, self.MD_API)

        shutil.copyfile(os.path.join(self.test_md_path(), "empty.md"), os.path.join(self.test_md_path(), "test.md"))
        self._test_result(self.empty_desc, self.empty_API)

        os.remove(os.path.join(self.test_md_path(), "test.md"))
        self._test_result(self.JS_desc, self.empty_API)

        # JS has API only, iterate through MD permutations
        shutil.copyfile(os.path.join(self.test_md_path(), "all.md"), os.path.join(self.test_md_path(), "test.md"))
        shutil.copyfile(os.path.join(self.test_js_path(), "api.js"), os.path.join(self.test_js_path(), "test.js"))
        self._test_result(self.MD_desc, self.MD_API)

        shutil.copyfile(os.path.join(self.test_md_path(), "desc.md"), os.path.join(self.test_md_path(), "test.md"))
        self._test_result(self.MD_desc, self.JS_API)

        shutil.copyfile(os.path.join(self.test_md_path(), "api.md"), os.path.join(self.test_md_path(), "test.md"))
        self._test_result(self.empty_desc, self.MD_API)

        shutil.copyfile(os.path.join(self.test_md_path(), "empty.md"), os.path.join(self.test_md_path(), "test.md"))
        self._test_result(self.empty_desc, self.JS_API)

        os.remove(os.path.join(self.test_md_path(), "test.md"))
        self._test_result(self.empty_desc, self.JS_API)

        # JS is empty, iterate through MD permutations
        shutil.copyfile(os.path.join(self.test_md_path(), "all.md"), os.path.join(self.test_md_path(), "test.md"))
        shutil.copyfile(os.path.join(self.test_js_path(), "empty.js"), os.path.join(self.test_js_path(), "test.js"))
        self._test_result(self.MD_desc, self.MD_API)

        shutil.copyfile(os.path.join(self.test_md_path(), "desc.md"), os.path.join(self.test_md_path(), "test.md"))
        self._test_result(self.MD_desc, self.empty_API)

        shutil.copyfile(os.path.join(self.test_md_path(), "api.md"), os.path.join(self.test_md_path(), "test.md"))
        self._test_result(self.empty_desc, self.MD_API)

        shutil.copyfile(os.path.join(self.test_md_path(), "empty.md"), os.path.join(self.test_md_path(), "test.md"))
        self._test_result(self.empty_desc, self.empty_API)

        os.remove(os.path.join(self.test_md_path(), "test.md"))
        self._test_result(self.empty_desc, self.empty_API)

        # clean up JS file
        os.remove(os.path.join(self.test_js_path(), "test.js"))

    def test_md_and_js_equivalence(self):
        # the Markdown parser and the in-source parser may produce different
        # JSON, but the rendered doc must be the same
        # maybe when the output of docstract is a bit more stable we should
        # require the JSON to be identical?
        md_path = os.path.join(self.sample_path(), "APIsample.md")
        module_json_md = apiparser_md.parse_api_doc(open(md_path).read())
        module_div_md = apirenderer.json_to_div(module_json_md, "APIsample")

        js_path = os.path.join(self.sample_path(), "APIsample.js")
        module_json_js = docstract.DocStract().extractFromFile(js_path)
        module_div_js = apirenderer.json_to_div(module_json_js, "APIsample")

        self.assertEqual(module_div_md, module_div_js)

    def MD_desc(self, json):
        self.assertEqual(md_desc, json["desc"])

    def JS_desc(self, json):
        self.assertEqual(js_desc, json["desc"])

    def empty_desc(self, json):
        self.assertEqual("", json["desc"])

    def MD_API(self, json):
        self.assertEqual(len(json["functions"]), 1)
        test_class = json["functions"][0]
        self.assertEqual(test_class["desc"], md_api)

    def JS_API(self, json):
        self.assertEqual(len(json["functions"]), 1)
        test_class = json["functions"][0]
        self.assertEqual(test_class["desc"], js_api)

    def empty_API(self, json):
        self.assertEqual(0, len(json["functions"]))

if __name__ == "__main__":
    unittest.main()
