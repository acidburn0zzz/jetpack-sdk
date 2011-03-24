import os
import unittest

from cuddlefish.apiparser import parse_hunks, ParseError
from cuddlefish.apirenderer import md_to_html
from HTMLParser import HTMLParser

tests_path = os.path.abspath(os.path.dirname(__file__))
static_files_path = os.path.join(tests_path, "static-files", "docs")
"""
'expected' is a list of dictionaries. Each dictionary item must contain a
string item called 'tag' and may contain a string item called 'data' and/or
an item called 'attrs' which is a list of tuples, corresponding to HTML
attributes.

The test is initialized with the first item in 'expected'. When the parser
finds an HTML element whose tag matches the 'tag' value for this item, we
execute the test for thhat element, using this 'expected' item.

Executing the test means:
- we test that each attribute in 'expected.attrs' matches an attribute in
the element.
- if 'expected' contains a value for 'data, then we also test that this
value matches any data immediately following the start tag and preceding
any other tags or the end tag.

If the test passes, we move on to the next expected item.

So: you can skip HTML elements by not including their tag. But you can't,
for example, skip a <div> element if the next tag you want to examine is
also a <div> element.
"""
expected = [
{"tag" : "div", "attrs" : [("id", "APIsample_module_api_docs"), ("class", "module_api_docs")]},
{"tag" : "h1", "data" : "APIsample"},
{"tag" : "div", "attrs" : [("class", "module_description")]},
{"tag" : "h1", "data" : "Title"},
{"tag" : "div", "attrs" : [("class", "api_reference")]},
{"tag" : "h2", "attrs" : [("class", "api_header")], "data" : "API Reference"},
# Classes
#--------
{"tag" : "div", "attrs" : [("class", "api_component_group")]},
{"tag" : "h3", "attrs" : [("class", "api_header")], "data" : "Classes"},
# class 1 is empty
{"tag" : "div", "attrs" : [("class", "api_component")]},
{"tag" : "h4", "attrs" : [("class", "api_name")], "data" : "empty-class"},
# class 2 has a single constructor
{"tag" : "div", "attrs" : [("class", "api_component")]},
{"tag" : "h4", "attrs" : [("class", "api_name")], "data" : "only-one-ctor"},
  # class 2's constructor group
  {"tag" : "div", "attrs" : [("class", "api_component_group")]},
  {"tag" : "div", "attrs" : [("class", "api_header")], "data" : "Constructors"},
  {"tag" : "div", "attrs" : [("class", "api_component")]},
  {"tag" : "div", "attrs" : [("class", "api_name")], "data" : "one-constructor(options)"},
  {"tag" : "div", "attrs" : [("class", "parameter_set")]},
  {"tag" : "div", "attrs" : [("class", "api_component")]},
  {"tag" : "div", "attrs" : [("class", "api_name")], "data" : "[ options ]"},
# class 3 has 2 ctors
{"tag" : "div", "attrs" : [("class", "api_component")]},
{"tag" : "h4", "attrs" : [("class", "api_name")], "data" : "two-ctors"},
# class 3's constructor group
  {"tag" : "div", "attrs" : [("class", "api_component_group")]},
  {"tag" : "div", "attrs" : [("class", "api_header")], "data" : "Constructors"},
  {"tag" : "div", "attrs" : [("class", "api_component")]},
  {"tag" : "div", "attrs" : [("class", "api_name")], "data" : "one-constructor(options)"},
  {"tag" : "div", "attrs" : [("class", "parameter_set")]},
  {"tag" : "div", "attrs" : [("class", "api_component")]},
  {"tag" : "div", "attrs" : [("class", "api_name")], "data" : "[ options ]"},
  {"tag" : "div", "attrs" : [("class", "api_component")]},
  {"tag" : "div", "attrs" : [("class", "api_name")], "data" : "another-constructor(options)"},
  {"tag" : "div", "attrs" : [("class", "parameter_set")]},
  {"tag" : "div", "attrs" : [("class", "api_component")]},
  {"tag" : "div", "attrs" : [("class", "api_name")], "data" : "[ options ]"},
# class 4 has 1 ctor, 1 method
{"tag" : "div", "attrs" : [("class", "api_component")]},
{"tag" : "h4", "attrs" : [("class", "api_name")], "data" : "ctor-and-method"},
# class 4's constructor group
  {"tag" : "div", "attrs" : [("class", "api_component_group")]},
  {"tag" : "div", "attrs" : [("class", "api_header")], "data" : "Constructors"},
  {"tag" : "div", "attrs" : [("class", "api_component")]},
  {"tag" : "div", "attrs" : [("class", "api_name")], "data" : "one-constructor(options)"},
  {"tag" : "div", "attrs" : [("class", "parameter_set")]},
  {"tag" : "div", "attrs" : [("class", "api_component")]},
  {"tag" : "div", "attrs" : [("class", "api_name")], "data" : "[ options ]"},
# class 4's method group
  {"tag" : "div", "attrs" : [("class", "api_component_group")]},
  {"tag" : "div", "attrs" : [("class", "api_header")], "data" : "Methods"},
  {"tag" : "div", "attrs" : [("class", "api_component")]},
  {"tag" : "div", "attrs" : [("class", "api_name")], "data" : "a-method(options)"},
  {"tag" : "div", "attrs" : [("class", "parameter_set")]},
  {"tag" : "div", "attrs" : [("class", "api_component")]},
  {"tag" : "div", "attrs" : [("class", "api_name")], "data" : "[ options ]"},
# class 5 has 1 ctor, 1 method, 1 property, 1 event
{"tag" : "div", "attrs" : [("class", "api_component")]},
{"tag" : "h4", "attrs" : [("class", "api_name")], "data" : "ctor-method-prop-event"},
# class 5's constructor group
  {"tag" : "div", "attrs" : [("class", "api_component_group")]},
  {"tag" : "div", "attrs" : [("class", "api_header")], "data" : "Constructors"},
  {"tag" : "div", "attrs" : [("class", "api_component")]},
  {"tag" : "div", "attrs" : [("class", "api_name")], "data" : "one-constructor(options)"},
  {"tag" : "div", "attrs" : [("class", "parameter_set")]},
  {"tag" : "div", "attrs" : [("class", "api_component")]},
  {"tag" : "div", "attrs" : [("class", "api_name")], "data" : "[ options ]"},
# class 5's method group
  {"tag" : "div", "attrs" : [("class", "api_component_group")]},
  {"tag" : "div", "attrs" : [("class", "api_header")], "data" : "Methods"},
  {"tag" : "div", "attrs" : [("class", "api_component")]},
  {"tag" : "div", "attrs" : [("class", "api_name")], "data" : "a-method(options)"},
  {"tag" : "div", "attrs" : [("class", "parameter_set")]},
  {"tag" : "div", "attrs" : [("class", "api_component")]},
  {"tag" : "div", "attrs" : [("class", "api_name")], "data" : "[ options ]"},
# class 5's property group
  {"tag" : "div", "attrs" : [("class", "api_component_group")]},
  {"tag" : "div", "attrs" : [("class", "api_header")], "data" : "Properties"},
  {"tag" : "div", "attrs" : [("class", "api_component")]},
  {"tag" : "div", "attrs" : [("class", "api_name")], "data" : "a-property : "},
# class 5's event group
  {"tag" : "div", "attrs" : [("class", "api_component_group")]},
  {"tag" : "div", "attrs" : [("class", "api_header")], "data" : "Events"},
  {"tag" : "div", "attrs" : [("class", "api_component")]},
  {"tag" : "div", "attrs" : [("class", "api_name")], "data" : "message"},
  {"tag" : "div", "attrs" : [("class", "parameter_set")]},
  {"tag" : "div", "attrs" : [("class", "api_component")]},
  {"tag" : "div", "attrs" : [("class", "api_name")], "data" : "JSON"},
# Functions
#----------
{"tag" : "div", "attrs" : [("class", "api_component_group")]},
{"tag" : "h3", "attrs" : [("class", "api_header")], "data" : "Functions"},
# function 1
{"tag" : "div", "attrs" : [("class", "api_component")]},
{"tag" : "h4", "attrs" : [("class", "api_name")], "data" : "test(argOne, argTwo, argThree, options)"},
  {"tag" : "div", "attrs" : [("class", "parameter_set")]},
  {"tag" : "div", "attrs" : [("class", "api_component")]},
  {"tag" : "div", "attrs" : [("class", "api_name")], "data" : "argOne : "},
  {"tag" : "span", "attrs" : [("class", "datatype")], "data" : "string"},
  {"tag" : "div", "attrs" : [("class", "api_component")]},
  {"tag" : "div", "attrs" : [("class", "api_name")], "data" : "[ argTwo : "},
  {"tag" : "span", "attrs" : [("class", "datatype")], "data" : "bool"},
  {"tag" : "div", "attrs" : [("class", "api_component")]},
  {"tag" : "div", "attrs" : [("class", "api_name")], "data" : "[ argThree = default : "},
  {"tag" : "span", "attrs" : [("class", "datatype")], "data" : "uri"},
  {"tag" : "div", "attrs" : [("class", "api_component")]},
  {"tag" : "div", "attrs" : [("class", "api_name")], "data" : "[ options ]"},
# function 2
{"tag" : "h4", "attrs" : [("class", "api_name")], "data" : "append(options)"},
  {"tag" : "div", "attrs" : [("class", "parameter_set")]},
  {"tag" : "div", "attrs" : [("class", "api_component")]},
  {"tag" : "div", "attrs" : [("class", "api_name")], "data" : "options"},
# function 3
{"tag" : "h4", "attrs" : [("class", "api_name")], "data" : "cool-func.dot(howMuch, double, options, onemore, options2)"},
  {"tag" : "div", "attrs" : [("class", "parameter_set")]},
  {"tag" : "div", "attrs" : [("class", "api_component")]},
  {"tag" : "div", "attrs" : [("class", "api_name")], "data" : "howMuch : "},
  {"tag" : "span", "attrs" : [("class", "datatype")], "data" : "string"},
# function 4
{"tag" : "h4", "attrs" : [("class", "api_name")], "data" : "random()"},
  {"tag" : "div", "attrs" : [("class", "returns")], "data" : "Returns: "},
  {"tag" : "span", "attrs" : [("class", "datatype")], "data" : "int"},
# Events
#-------
{"tag" : "h3", "attrs" : [("class", "api_header")], "data" : "Events"},
{"tag" : "div", "attrs" : [("class", "api_component")]},
{"tag" : "h4", "attrs" : [("class", "api_name")], "data" : "open"},
  {"tag" : "div", "attrs" : [("class", "parameter_set")]},
  {"tag" : "div", "attrs" : [("class", "api_component")]},
  {"tag" : "div", "attrs" : [("class", "api_name")]},
  {"tag" : "span", "attrs" : [("class", "datatype")], "data" : "bool"},

# this goes last: nothing after this will be tested
{"tag" : "nomatch"}
]

class TestElement(object):
    def __init__(self, expected, tester):
        self.expected_data = None
        self.expected = expected
        self.tester = tester

    def tag(self):
        return self.expected["tag"]

    def data(self):
        return self.expected.get("data", None)

    def _test_attrs(self, attrs):
        expected_attrs = self.expected.get("attrs", None)
        if not expected_attrs:
            return
        for expected_attr in expected_attrs:
            self.tester.assertTrue(expected_attr in attrs)

class HTMLChecker(HTMLParser):
    def __init__(self, tester):
        HTMLParser.__init__(self)
        self.tester = tester
        self.expected_index = 0
        self.expected = TestElement(expected[self.expected_index], self.tester)
        self.expected_data = None

    def handle_starttag(self, tag, attrs):
        if tag == self.expected.tag():
            self.expected._test_attrs(attrs)
            self.expected_data = self.expected.data()
            self.expected_index = self.expected_index + 1
            self.expected = TestElement(expected[self.expected_index], self.tester)

    def handle_data(self, data):
        if self.expected_data:
            self.tester.assertEqual(self.expected_data, data)
            self.expected_data = None

class RendererTests(unittest.TestCase):
    def test_renderer(self):
        test = md_to_html(os.path.join(static_files_path, "APIsample.md"))
        html_checker = HTMLChecker(self)
        html_checker.feed(test)

if __name__ == "__main__":
    unittest.main()
