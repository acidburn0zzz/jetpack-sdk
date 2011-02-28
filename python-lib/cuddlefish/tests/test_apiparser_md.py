
import os
import unittest
import simplejson
from cuddlefish import apiparser_md

tests_path = os.path.abspath(os.path.dirname(__file__))
static_files_path = os.path.join(tests_path, "static-files")

class MD_ParserTests(unittest.TestCase):
    def pathname(self, filename):
        return os.path.join(static_files_path, "docs", filename)

    def parse_text(self, text):
        return apiparser_md.parse_api_doc(text)

    def parse(self, pathname):
        return apiparser_md.parse_api_doc(open(pathname).read())

    def test_parser(self):
        module_json = self.parse(self.pathname("APIsample.md"))
        test_json = simplejson.dumps(module_json, indent=2)
        reference_json = open(self.pathname("APIsample.json")).read()
        self.assertEqual(test_json, reference_json)

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
        self.assertRaises(apiparser_md.ParseError, self.parse_text, md)

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
        self.assertRaises(apiparser_md.ParseError, self.parse_text, md)

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
        parsed = self.parse_text(md)
        r = parsed["functions"][0]["returns"]
        self.assertEqual(r["properties"][0]["name"], "firststring")
        self.assertEqual(r["properties"][0],
                         {"name": "firststring",
                          "type": "string",
                          "desc": "First string.",
                          "line_number": 5, # 1-indexed
                          })
        self.assertEqual(r["properties"][1],
                         {"name": "[firsturl]",
                          "type": "url",
                          "desc": "First URL, not always provided.",
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
        parsed = self.parse_text(md)
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
        parsed = self.parse_text(md)
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
        parsed = self.parse_text(md)
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
        parsed = self.parse_text(md)
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
        self.assertRaises(apiparser_md.ParseError, self.parse_text, md)

    def test_missing_apitype(self):
        md = '''\
<api name="test">
Sorry, you must have a @method or something before the description.
Putting it after the description is not good enough
@method
@returns something
</api>
'''
        self.assertRaises(apiparser_md.ParseError, self.parse_text, md)

    def test_missing_param_propname(self):
        md = '''\
<api name="test">
@method
This is a function which does nothing in particular.
@param p1 {object} This is a parameter.
  @prop {string} Oops, props must have a name.
</api>
'''
        self.assertRaises(apiparser_md.ParseError, self.parse_text, md)

    def test_missing_param_proptype(self):
        md = '''\
<api name="test">
@method
This is a function which does nothing in particular.
@param p1 {object} This is a parameter.
  @prop name Oops, props must have a type.
</api>
'''
        self.assertRaises(apiparser_md.ParseError, self.parse_text, md)

    def test_property(self):
        md = '''\
<api name="test">
@property {foo}
An object property named test of type foo.
</api>
'''
        parsed = self.parse_text(md)
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
        self.assertRaises(apiparser_md.ParseError, self.parse_text, md)

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
        self.assertRaises(apiparser_md.ParseError, self.parse_text, md)

if __name__ == "__main__":
    unittest.main()
