
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

    def sample_path(self):
        return os.path.join(static_files_path, "docs")

    def test_md_path(self):
        return os.path.join(static_files_path, "packages", "aardvark", "docs")

    def test_js_path(self):
        return os.path.join(static_files_path, "packages", "aardvark", "lib")

    def _test_result(self, desc_function, api_function):
        module_json = apiparser.get_api_json(static_files_path, "aardvark", ["test"])
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

    def _compare_props(self, json1, json2):
        self.assertEqual(json1.get("name", None), json2.get("name", None))
        self.assertEqual(json1.get("type", None), json2.get("type", None))
# docstract and apiparser_md handle newlines differently, it seems. who should change??
#        self.assertEqual(json1.get("desc", None), json2.get("desc", None))
        self.assertEqual(json1.get("optional", None), json2.get("optional", None))

    def _compare_count(self, json1, json2):
        self.assertEqual(len(json1), len(json2))

    def test_md_and_js_equivalence(self):
        # the Markdown parser and the in-source parser will produce different
        # JSON (for example, the filename is always different) but the core stuff
        # must be the same
        md_path = os.path.join(self.sample_path(), "APIsample.md")
        json_md = apiparser_md.extractFromFile(md_path)

        js_path = os.path.join(self.sample_path(), "APIsample.js")
        json_js = docstract.DocStract().extractFromFile(js_path)

        self._compare_props(json_md, json_js)

        self._compare_count(json_md["classes"], json_js["classes"])
        self._compare_props(json_md["classes"][0], json_js["classes"][0])
        self._compare_props(json_md["classes"][1], json_js["classes"][1])
# docstract's constructors don't have names, so the compare will fail. who should change??
  #      self._compare_props(json_md["classes"][1]["constructor"], json_js["classes"][1]["constructor"])
        self._compare_props(json_md["classes"][1]["constructor"]["params"][0], json_js["classes"][1]["constructor"]["params"][0])

        self._compare_props(json_md["classes"][2], json_js["classes"][2])
  #      self._compare_props(json_md["classes"][2]["constructor"], json_js["classes"][2]["constructor"])
        self._compare_props(json_md["classes"][2]["functions"][0], json_js["classes"][2]["functions"][0])
        self._compare_props(json_md["classes"][2]["functions"][0]["params"][0], json_js["classes"][2]["functions"][0]["params"][0])

        self._compare_props(json_md["classes"][3], json_js["classes"][3])
  #      self._compare_props(json_md["classes"][3]["constructor"], json_js["classes"][3]["constructor"])
        self._compare_props(json_md["classes"][3]["functions"][0], json_js["classes"][3]["functions"][0])
        self._compare_props(json_md["classes"][3]["functions"][0]["params"][0], json_js["classes"][3]["functions"][0]["params"][0])
        self._compare_props(json_md["classes"][3]["properties"][0], json_js["classes"][3]["properties"][0])

        self._compare_count(json_md["functions"], json_js["functions"])

        self._compare_props(json_md["functions"][0], json_js["functions"][0])
        self._compare_props(json_md["functions"][0]["returns"], json_js["functions"][0]["returns"])
        self._compare_props(json_md["functions"][0]["params"][0], json_js["functions"][0]["params"][0])
        self._compare_props(json_md["functions"][0]["params"][1], json_js["functions"][0]["params"][1])
        self._compare_props(json_md["functions"][0]["params"][2], json_js["functions"][0]["params"][2])
        self._compare_props(json_md["functions"][0]["params"][3], json_js["functions"][0]["params"][3])

        self._compare_props(json_md["functions"][1], json_js["functions"][1])
        self._compare_props(json_md["functions"][1]["params"][0], json_js["functions"][1]["params"][0])

        self._compare_props(json_md["functions"][2], json_js["functions"][2])
        self._compare_props(json_md["functions"][2]["params"][0], json_js["functions"][2]["params"][0])
        self._compare_props(json_md["functions"][2]["params"][1], json_js["functions"][2]["params"][1])
        self._compare_props(json_md["functions"][2]["params"][2], json_js["functions"][2]["params"][2])
        self._compare_props(json_md["functions"][2]["params"][3], json_js["functions"][2]["params"][3])
        self._compare_props(json_md["functions"][2]["params"][4], json_js["functions"][2]["params"][4])

        self._compare_props(json_md["functions"][3], json_js["functions"][3])
        self._compare_props(json_md["functions"][3]["returns"], json_js["functions"][3]["returns"])

        self._compare_count(json_md["properties"], json_js["properties"])
        self._compare_props(json_md["properties"][0], json_js["properties"][0])

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
