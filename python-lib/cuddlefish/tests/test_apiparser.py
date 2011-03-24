
import os
import unittest
from cuddlefish.apiparser import parse_hunks, ParseError

tests_path = os.path.abspath(os.path.dirname(__file__))
static_files_path = os.path.join(tests_path, "static-files")

tests_path = os.path.abspath(os.path.dirname(__file__))
static_files_path = os.path.join(tests_path, "static-files")

class MD_ParserTests(unittest.TestCase):
    def pathname(self, filename):
        return os.path.join(static_files_path, "docs", filename)

    def parse_text(self, text):
        return list(parse_hunks(text))

    def parse(self, pathname):
        return self.parse_text(open(pathname).read())

    def _test_json(self, function_json, **kwargs):
        for key in kwargs:
            self.assertEqual(function_json[key], kwargs[key])

    # this function only exists so the test code lines up, to make it easier to read
    def _testLength(self, item, length):
        self.assertEqual(len(item), length)

    def test_parser(self):
        module_json = self.parse(self.pathname("APIsample.md"))
        version_json = module_json[0]
        self.assertEqual(module_json[0], ("version", 4))
        self.assertEqual(module_json[1],
                         ("markdown", "# Title #\n\nSome text here\n\n"))
        self.assertEqual(module_json[2][0], "api-json")
        # function 1
        function_1 = module_json[2][1]
        self._test_json(function_1, type="function",
                                    name="test",
                                    signature="test(argOne, argTwo, argThree, options)",
                                    description="This is a function which does nothing in particular.")
        self._test_json(function_1["params"][0], datatype="string",
                                              required=True,
                                              name="argOne",
                                              description="This is the first argument.")
        self._test_json(function_1["params"][1], datatype="bool",
                                              required=False,
                                              name="argTwo",
                                              description="This is the second argument.")
        self._test_json(function_1["params"][2], datatype="uri",
                                              required=False,
                                              name="argThree",
                                              description="This is the third and final argument. And this is\na test of the ability to do multiple lines of\ntext.")
        self._test_json(function_1["params"][3], required=False,
                                              name="options",
                                              description="Options Bag")
        self._test_json(function_1["params"][3]["props"][0], datatype="string",
                                                          required=False,
                                                          name="style",
                                                          description="Some style information.")
        self._test_json(function_1["params"][3]["props"][1], datatype="bool",
                                                          required=False,
                                                          default="True",
                                                          name="secondToLastOption",
                                                          description="The last property.")
        self._test_json(function_1["params"][3]["props"][2], datatype="uri",
                                                          required=False,
                                                          name="lastOption",
                                                          description="And this time we have\nA multiline description\nWritten as haiku")
        self._test_json(function_1["returns"], datatype="object")
        # function 2
        function_2 = module_json[4][1]
        self._test_json(function_2, type="function",
                                    name="append",
                                    signature="append(options)",
                                    description="This is a list of options to specify modifications to your slideBar instance.")
        self._test_json(function_2["params"][0], required=True,
                                                 name="options",
                                                 description="Pass in all of your options here.")
        self._test_json(function_2["params"][0]["props"][0], datatype="uri",
                                                             required=False,
                                                             name="icon",
                                                             description="The HREF of an icon to show as the method of accessing your features slideBar")
        self._test_json(function_2["params"][0]["props"][1], datatype="string/xml",
                                                             required=False,
                                                             name="html",
                                                             description="The content of the feature, either as an HTML string,\nor an E4X document fragment.")
        self._test_json(function_2["params"][0]["props"][2], datatype="uri",
                                                             required=False,
                                                             name="url",
                                                             description="The url to load into the content area of the feature")
        self._test_json(function_2["params"][0]["props"][3], datatype="int",
                                                             required=False,
                                                             name="width",
                                                             description="Width of the content area and the selected slide size")
        self._test_json(function_2["params"][0]["props"][4], datatype="bool",
                                                             required=False,
                                                             name="persist",
                                                             description="Default slide behavior when being selected as follows:\nIf true: blah; If false: double blah.")
        self._test_json(function_2["params"][0]["props"][5], datatype="bool",
                                                             required=False,
                                                             name="autoReload",
                                                             description="Automatically reload content on select")
        self._test_json(function_2["params"][0]["props"][6], datatype="function",
                                                             required=False,
                                                             name="onClick",
                                                             description="Callback when the icon is clicked")
        self._test_json(function_2["params"][0]["props"][7], datatype="function",
                                                             required=False,
                                                             name="onSelect",
                                                             description="Callback when the feature is selected")
        self._test_json(function_2["params"][0]["props"][8], datatype="function",
                                                             required=False,
                                                             name="onReady",
                                                             description="Callback when featured is loaded")
        # function 3
        function_3 = module_json[6][1]
        self._test_json(function_3, type="function",
                                    name="cool-func.dot",
                                    signature="cool-func.dot(howMuch, double, options, onemore, options2)",
                                    description="")
        self._test_json(function_3["params"][0], datatype="string",
                                                 required=True,
                                                 name="howMuch",
                                                 description="How much cool it is.")
        self._test_json(function_3["params"][1], datatype="bool",
                                                 required=False,
                                                 default="true",
                                                 name="double",
                                                 description="In case you just really need to double it.")
        self._test_json(function_3["params"][2], required=False,
                                                 name="options",
                                                 description="An object-bag of goodies.")
        self._test_json(function_3["params"][3], datatype="bool",
                                                 required=False,
                                                 name="onemore",
                                                 description="One more paramater")
        self._test_json(function_3["params"][4], required=False,
                                                 name="options2",
                                                 description="This is a full description of something\nthat really sucks. Because I now have a multiline\ndescription of this thingy.")
        self._test_json(function_3["returns"], datatype="string",
                                               description="A value telling you just how cool you are.\nA boa-constructor!\n" + \
                                                         "This description can go on for a while, and can even contain\nsome **realy** fancy things. " + \
                                                         "Like `code`, or even\n~~~~{.javascript}\n// Some code!\n~~~~")
        # function 4
        function_4 = module_json[8][1]
        self._test_json(function_4, type="function",
                                    name="random",
                                    signature="random()",
                                    description="A function that returns a random integer between 0 and 10.")
        self._test_json(function_4["returns"], datatype="int",
                                               description="The random number.")
        # class 1 is empty
        class_1 = module_json[10][1]
        self._test_json(class_1, type="class",
                                 name="empty-class",
                                 description="This class contains nothing.")
        # class 2
        class_2 = module_json[12][1]
        self._test_json(class_2, type="class",
                                 name="only-one-ctor",
                                 description="This class contains only one constructor.")
        self._test_json(class_2["constructors"][0], type="constructor",
                                                    name="one-constructor",
                                                    signature="one-constructor(options)",
                                                    description="")
        self._test_json(class_2["constructors"][0]["params"][0], name="options",
                                                                 required=False,
                                                                 description="An object-bag of goodies.")
        # class 3
        class_3 = module_json[14][1]
        self._test_json(class_3, type="class",
                                 name="two-ctors",
                                 description="This class contains two constructors.")
        self._test_json(class_3["constructors"][0], type="constructor",
                                                    name="one-constructor",
                                                    signature="one-constructor(options)",
                                                    description="The first constructor.")
        self._test_json(class_3["constructors"][0]["params"][0], name="options",
                                                                 required=False,
                                                                 description="An object-bag of goodies.")
        self._test_json(class_3["constructors"][1], type="constructor",
                                                    name="another-constructor",
                                                    signature="another-constructor(options)",
                                                    description="The second constructor.")
        self._test_json(class_3["constructors"][1]["params"][0], name="options",
                                                                 required=False,
                                                                 description="An object-bag of goodies.")
        # class 4
        class_4 = module_json[16][1]
        self._test_json(class_4, type="class",
                                 name="ctor-and-method",
                                 description="This class contains one constructor and one method.")
        self._test_json(class_4["constructors"][0], type="constructor",
                                                    name="one-constructor",
                                                    signature="one-constructor(options)",
                                                    description="The first constructor.")
        self._test_json(class_4["constructors"][0]["params"][0], name="options",
                                                                 required=False,
                                                                 description="An object-bag of goodies.")
        self._test_json(class_4["methods"][0], type="method",
                                               name="a-method",
                                               signature="a-method(options)",
                                               description="Does things.")
        self._test_json(class_4["methods"][0]["params"][0], name="options",
                                                            required=False,
                                                            description="An argument.")
        # class 4
        class_4 = module_json[18][1]
        self._test_json(class_4, type="class",
                                 name="ctor-method-prop-event",
                                 description="This class contains one constructor, one method, one property and an event.")
        self._test_json(class_4["constructors"][0], type="constructor",
                                                    name="one-constructor",
                                                    signature="one-constructor(options)",
                                                    description="The first constructor.")
        self._test_json(class_4["constructors"][0]["params"][0], name="options",
                                                                 required=False,
                                                                 description="An object-bag of goodies.")
        self._test_json(class_4["methods"][0], type="method",
                                               name="a-method",
                                               signature="a-method(options)",
                                               description="Does things.")
        self._test_json(class_4["methods"][0]["params"][0], name="options",
                                                            required=False,
                                                            description="An argument.")
        self._test_json(class_4["events"][0], type="event",
                                              name="message",
                                              description="Event emitted when the content script sends a message to the add-on.")
        self._test_json(class_4["events"][0]["arguments"][0], datatype="JSON",
                                                              description="The message itself as a JSON-serialized object.")
        # event 1
        event_1 = module_json[20][1]
        self._test_json(event_1, type="event",
                                 name="open",
                                 description="A module-level event called open.")
        self._test_json(event_1["arguments"][0], datatype="bool",
                                                 description="Yes, it's open.")

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
        self.assertRaises(ParseError, self.parse_text, md)

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
        self.assertRaises(ParseError, self.parse_text, md)

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
        r = parsed[1][1]["returns"]
        self.assertEqual(r["props"][0]["name"], "firststring")
        self.assertEqual(r["props"][0],
                         {"name": "firststring",
                          "datatype": "string",
                          "description": "First string.",
                          "required": True,
                          "line_number": 5, # 1-indexed
                          })
        self.assertEqual(r["props"][1],
                         {"name": "firsturl",
                          "datatype": "url",
                          "description": "First URL, not always provided.",
                          "required": False,
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
        r = parsed[1][1]["returns"]
        self.assertEqual(r["description"], "A one-line description.")

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
        r = parsed[1][1]["returns"]
        self.assertEqual(r["description"],
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
        r = parsed[1][1]["returns"]
        self.assertEqual(r["description"], "A one-line untyped description.")

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
        r = parsed[1][1]["returns"]
        self.assertEqual(r["description"],
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
        self.assertRaises(ParseError, self.parse_text, md)

    def test_missing_apitype(self):
        md = '''\
<api name="test">
Sorry, you must have a @method or something before the description.
Putting it after the description is not good enough
@method
@returns something
</api>
'''
        self.assertRaises(ParseError, self.parse_text, md)

    def test_missing_param_propname(self):
        md = '''\
<api name="test">
@method
This is a function which does nothing in particular.
@param p1 {object} This is a parameter.
  @prop {string} Oops, props must have a name.
</api>
'''
        self.assertRaises(ParseError, self.parse_text, md)

    def test_missing_param_proptype(self):
        md = '''\
<api name="test">
@method
This is a function which does nothing in particular.
@param p1 {object} This is a parameter.
  @prop name Oops, props must have a type.
</api>
'''
        self.assertRaises(ParseError, self.parse_text, md)

    def test_property(self):
        md = '''\
<api name="test">
@property {foo}
An object property named test of type foo.
</api>
'''
        parsed = self.parse_text(md)
        self.assertEqual(parsed[1][0], 'api-json')
        actual_api_json_obj = parsed[1][1]
        expected_api_json_obj = {
            'line_number': 1,
            'datatype': 'foo',
            'type': 'property',
            'name': 'test',
            'description': "An object property named test of type foo."
            }
        self.assertEqual(actual_api_json_obj, expected_api_json_obj)

    def test_property_no_type(self):
        md = '''\
<api name="test">
@property
This property needs to specify a type!
</api>
'''
        self.assertRaises(ParseError, self.parse_text, md)

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
        self.assertRaises(ParseError, self.parse_text, md)

if __name__ == "__main__":
    unittest.main()
