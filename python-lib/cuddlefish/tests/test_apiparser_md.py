# These tests test the apiparser_md module, whose job is to extract JSON
# from specially formatted markdown.
#
# We'll:
# - generate JSON from a sample MD file and check it looks reasonable
# - use specially crafted MD to test some corner cases and exceptions
#
# These lines exceed 80 characters in some places for the sake of making it
# much, much easier to read.

import os
import unittest
import simplejson
from cuddlefish import apiparser_md

tests_path = os.path.abspath(os.path.dirname(__file__))
static_files_path = os.path.join(tests_path, "static-files")

class MD_ParserTests(unittest.TestCase):
    def pathname(self, filename):
        return os.path.join(static_files_path, "docs", filename)

    def _test_props(self, json, name, api_type, desc, optional):
        self.assertEqual(json.get("name", None), name)
        self.assertEqual(json.get("type", None), api_type)
        self.assertEqual(json.get("desc", None), desc)
        self.assertEqual(json.get("optional", None), optional)

    # this function only exists so the test code lines up, to make it easier to read
    def _testLength(self, item, length):
        self.assertEqual(len(item), length)

    def test_parser(self):
        module_json = apiparser_md.extractFromFile(self.pathname("APIsample.md"))
# module-level stuff
        self.assertEqual(module_json["module"], "APIsample")
        self.assertEqual(module_json["filename"], self.pathname("APIsample.md"))
        self.assertEqual(module_json["desc"], "# Title #\n\nSome text here\n\n")
# properties
        self.assertEqual(len(module_json["properties"]), 1)
        self._test_props(module_json["properties"][0], "test_property", "string", "It's a string.", None)
# functions: we'll only look in detail at the first couple of functions
        self.assertEqual(len(module_json["functions"]), 4)

        self.assertEqual(module_json["functions"][0]["name"], "test")
        self.assertEqual(module_json["functions"][0]["desc"], "This is a function which does nothing in particular.")

        self.assertEqual(module_json["functions"][0]["returns"]["type"], "object")
        self._testLength(module_json["functions"][0]["returns"]["properties"], 2)
        self._test_props(module_json["functions"][0]["returns"]["properties"][0], "firststring", "string", "First string", None)
        self._test_props(module_json["functions"][0]["returns"]["properties"][1], "firsturl", "url", "First URL", None)

        self._testLength(module_json["functions"][0]["params"], 4)
        self._test_props(module_json["functions"][0]["params"][0], "argOne", "string", "This is the first argument.", None)
        self._test_props(module_json["functions"][0]["params"][1], "argTwo", "bool", "This is the second argument.", True)
        self._test_props(module_json["functions"][0]["params"][2], \
                         "argThree=default", "uri", "This is the third and final " + \
                          "argument. And this is\na test of the ability to do " + \
                          "multiple lines of\ntext.", True)
        self._test_props(module_json["functions"][0]["params"][3], "options", None, "Options Bag", True)
        self._testLength(module_json["functions"][0]["params"][3]["properties"], 3)
        self._test_props(module_json["functions"][0]["params"][3]["properties"][0], "style", "string", "Some style information.", True)
        self._test_props(module_json["functions"][0]["params"][3]["properties"][1], "secondToLastOption=True", "bool", "The last property.", True)
        self._test_props(module_json["functions"][0]["params"][3]["properties"][2], \
                                     "lastOption", "uri", "And this time we have\nA multiline description\nWritten as haiku", True)

        self.assertEqual(module_json["functions"][1]["name"], "append")
        self.assertEqual(module_json["functions"][1]["desc"], "This is a list of options to specify modifications to your slideBar instance.")

        self._testLength(module_json["functions"][1]["params"], 1)
        self._test_props(module_json["functions"][1]["params"][0], "options", None, "Pass in all of your options here.", None)
        self._testLength(module_json["functions"][1]["params"][0]["properties"], 9)
        self._test_props(module_json["functions"][1]["params"][0]["properties"][0], \
                         "icon", "uri", "The HREF of an icon to show as the method of accessing your features slideBar", True)
        self._test_props(module_json["functions"][1]["params"][0]["properties"][1], \
                         "html", "string/xml", "The content of the feature, either as an HTML string,\n" + \
                         "or an E4X document fragment (e.g., <><h1>Hi!</h1></>)", True)
        self._test_props(module_json["functions"][1]["params"][0]["properties"][2], \
                         "url", "uri", "The url to load into the content area of the feature", True)
        self._test_props(module_json["functions"][1]["params"][0]["properties"][3], \
                         "width", "int", "Width of the content area and the selected slide size", True)
        self._test_props(module_json["functions"][1]["params"][0]["properties"][4], \
                         "persist", "bool", "Default slide behavior when being selected as follows:\n" + \
                         "If true: blah; If false: double blah.", True)
        self._test_props(module_json["functions"][1]["params"][0]["properties"][5], \
                         "autoReload", "bool", "Automatically reload content on select", True)
        self._test_props(module_json["functions"][1]["params"][0]["properties"][6], \
                         "onClick", "function", "Callback when the icon is clicked", True)
        self._test_props(module_json["functions"][1]["params"][0]["properties"][7], \
                         "onSelect", "function", "Callback when the feature is selected", True)
        self._test_props(module_json["functions"][1]["params"][0]["properties"][8], \
                         "onReady", "function", "Callback when featured is loaded", True)
# classes
        self._testLength(module_json["classes"], 4)

        self._test_props(module_json["classes"][0], "empty_class", None, "This class contains nothing.", None)

        self._test_props(module_json["classes"][1], "only_one_ctor", None, "This class contains only one constructor.", None)
        self._test_props(module_json["classes"][1]["constructor"], "only_one_ctor", None, "", None)
        self._test_props(module_json["classes"][1]["constructor"]["params"][0], "options", None, "An object-bag of goodies.", True)

        self._test_props(module_json["classes"][2], "ctor_and_method", None, "This class contains one constructor and one method.", None)
        self._test_props(module_json["classes"][2]["constructor"], "ctor_and_method", None, "The first constructor.", None)
        self._test_props(module_json["classes"][2]["constructor"]["params"][0], "options", None, "An object-bag of goodies.", True)
        self._testLength(module_json["classes"][2]["functions"], 1)
        self._test_props(module_json["classes"][2]["functions"][0], "a_method", None, "Does things.", None)
        self._test_props(module_json["classes"][2]["functions"][0]["params"][0], "options", None, "An argument.", True)

        self._test_props(module_json["classes"][3], "ctor_and_method_and_prop", None, "This class contains one constructor, one method, and one property.", None)
        self._test_props(module_json["classes"][3]["constructor"], "ctor_and_method_and_prop", None, "The first constructor.", None)
        self._test_props(module_json["classes"][3]["constructor"]["params"][0], "options", None, "An object-bag of goodies.", True)
        self._testLength(module_json["classes"][3]["functions"], 1)
        self._test_props(module_json["classes"][3]["functions"][0], "a_method", None, "Does things.", None)
        self._test_props(module_json["classes"][3]["functions"][0]["params"][0], "options", None, "An argument.", True)
        self._testLength(module_json["classes"][3]["properties"], 1)
        self._test_props(module_json["classes"][3]["properties"][0], "a_property", "bool", "Represents stuff.", None)

    def test_missing_return_propname(self):
        md = '''\
<api name="test">
@method
This is a function which does nothing in particular.
@returns {object}
  @prop {string} First string, but the property name is missing
  @prop {url} First URL, same problem
@param argOne {string} This is the first argument.
</api>
'''
        self.assertRaises(apiparser_md.ParseError, apiparser_md.extract, md)

    def test_missing_return_proptype(self):
        md = '''\
<api name="test">
@method
This is a function which does nothing in particular.
@returns {object}
  @prop untyped It is an error to omit the type of a return property.
@param argOne {string} This is the first argument.
@param [argTwo=True] {bool} This is the second argument.
</api>
'''
        self.assertRaises(apiparser_md.ParseError, apiparser_md.extract, md)

    def test_return_propnames(self):
        md = '''\
<api name="test">
@method
This is a function which does nothing in particular.
@returns {object}
  @prop firststring {string} First string.
  @prop [firsturl] {url} First URL, not always provided.
@param argOne {string} This is the first argument.
@param [argTwo=True] {bool} This is the second argument.
</api>
'''
        parsed = apiparser_md.extract(md)
        r = parsed["functions"][0]["returns"]
        self.assertEqual(r["properties"][0]["name"], "firststring")
        self.assertEqual(r["properties"][0],
                         {"name": "firststring",
                          "type": "string",
                          "desc": "First string.",
                          "line_number": 5, # 1-indexed
                          })
        self.assertEqual(r["properties"][1],
                         {"name": "firsturl",
                          "type": "url",
                          "desc": "First URL, not always provided.",
                          "optional": True,
                          "line_number": 6,
                          })

    def test_return_description_1(self):
        md = '''\
<api name="test">
@method
This is a function which does nothing in particular.
@returns {object} A one-line description.
  @prop firststring {string} First string.
  @prop [firsturl] {url} First URL, not always provided.
@param argOne {string} This is the first argument.
@param [argTwo=True] {bool} This is the second argument.
</api>
'''
        parsed = apiparser_md.extract(md)
        r = parsed["functions"][0]["returns"]
        self.assertEqual(r["desc"], "A one-line description.")

    def test_return_description_2(self):
        md = '''\
<api name="test">
@method
This is a function which does nothing in particular.
@returns {object} A six-line description
  which is consistently indented by two spaces
    except for this line
  and preserves the following empty line
  
  from which a two-space indentation will be removed.
  @prop firststring {string} First string.
  @prop [firsturl] {url} First URL, not always provided.
@param argOne {string} This is the first argument.
@param [argTwo=True] {bool} This is the second argument.
</api>
'''
        parsed = apiparser_md.extract(md)
        r = parsed["functions"][0]["returns"]
        self.assertEqual(r["desc"],
                         "A six-line description\n"
                         "which is consistently indented by two spaces\n"
                         "  except for this line\n"
                         "and preserves the following empty line\n"
                         "\n"
                         "from which a two-space indentation will be removed.")

    def test_return_description_3(self):
        md = '''\
<api name="test">
@method
This is a function which does nothing in particular.
@returns A one-line untyped description.
@param argOne {string} This is the first argument.
@param [argTwo=True] {bool} This is the second argument.
</api>
'''
        parsed = apiparser_md.extract(md)
        r = parsed["functions"][0]["returns"]
        self.assertEqual(r["desc"], "A one-line untyped description.")

    # if the return value was supposed to be an array, the correct syntax
    # would not have any @prop tags:
    #  @returns {array}
    #   Array consists of two elements, a string and a url...

    def test_return_array(self):
        md = '''\
<api name="test">
@method
This is a function which returns an array.
@returns {array}
  Array consists of two elements, a string and a url.
@param argOne {string} This is the first argument.
@param [argTwo=True] {bool} This is the second argument.
</api>
'''
        parsed = apiparser_md.extract(md)
        r = parsed["functions"][0]["returns"]
        self.assertEqual(r["desc"],
                         "Array consists of two elements, a string and a url.")

    def test_bad_default_on_required_parameter(self):
        md = '''\
<api name="test">
@method
This is a function which does nothing in particular.
@returns something
@param argOne=ILLEGAL {string} Mandatory parameters do not take defaults.
@param [argTwo=Chicago] {string} This is the second argument.
</api>
'''
        self.assertRaises(apiparser_md.ParseError, apiparser_md.extract, md)

    def test_missing_apitype(self):
        md = '''\
<api name="test">
Sorry, you must have a @method or something before the description.
Putting it after the description is not good enough
@method
@returns something
</api>
'''
        self.assertRaises(apiparser_md.ParseError, apiparser_md.extract, md)

    def test_missing_param_propname(self):
        md = '''\
<api name="test">
@method
This is a function which does nothing in particular.
@param p1 {object} This is a parameter.
  @prop {string} Oops, props must have a name.
</api>
'''
        self.assertRaises(apiparser_md.ParseError, apiparser_md.extract, md)

    def test_missing_param_proptype(self):
        md = '''\
<api name="test">
@method
This is a function which does nothing in particular.
@param p1 {object} This is a parameter.
  @prop name Oops, props must have a type.
</api>
'''
        self.assertRaises(apiparser_md.ParseError, apiparser_md.extract, md)

    def test_property(self):
        md = '''\
<api name="test">
@property {foo}
An object property named test of type foo.
</api>
'''
        parsed = apiparser_md.extract(md)
        actual_api_json_obj = parsed["properties"][0]
        expected_api_json_obj = {
            'line_number': 1,
            'type': 'foo',
            'name': 'test',
            'desc': "An object property named test of type foo."
            }
        self.assertEqual(actual_api_json_obj, expected_api_json_obj)

    def test_property_no_type(self):
        md = '''\
<api name="test">
@property
This property needs to specify a type!
</api>
'''
        self.assertRaises(apiparser_md.ParseError, apiparser_md.extract, md)

    def test_missing_api_closing_tag(self):
        md = '''\
<api name="test">
@class
This is a class with a missing closing tag.
<api name="doStuff"
@method
This method does stuff.
</api>
'''
        self.assertRaises(apiparser_md.ParseError, apiparser_md.extract, md)

if __name__ == "__main__":
    unittest.main()
