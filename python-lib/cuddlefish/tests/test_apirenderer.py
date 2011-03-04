
import os
import unittest

from cuddlefish import apiparser_md
from cuddlefish import apirenderer
from cuddlefish import docstract
from cuddlefish import BeautifulSoup

test_files_path = \
    os.path.join(os.path.abspath\
        (os.path.dirname(__file__)), "static-files", "docs")

class ParserTests(unittest.TestCase):

    def test_renderer(self):
        self.validate_html(self.get_html_md())
        self.validate_html(self.get_html_js())

    def get_html_md(self):
        md_path = os.path.join(test_files_path, "APIsample.md")
        json_md = apiparser_md.extractFromFile(md_path)
        html_md = apirenderer.json_to_html(json_md)
        return html_md

    def get_html_js(self):
        js_path = os.path.join(test_files_path, "APIsample.js")
        json_js = docstract.DocStract().extractFromFile(js_path)
        html_js = apirenderer.json_to_html(json_js)
        return html_js

    def validate_html(self, html):
# we won't test everything in here, just the basic structure of the doc
        soup = BeautifulSoup.BeautifulSoup(html)
        self.assertEqual(soup.html.body.div["id"], "APIsample_module_api_docs")
        self.assertEqual(soup.html.body.div["class"], "module_api_docs")
        self.assertEqual(soup.html.body.div.h1.string, unicode("APIsample"))
        top_level_divs = soup.html.body.div("div", recursive = False)

        module_desc = top_level_divs[0]
        self.assertEqual(module_desc["class"], "module_description")
        self.assertEqual(module_desc.h1.string, unicode("Title"))

        api_ref = top_level_divs[1]
        self.assertEqual(api_ref["class"], "api_reference")
        self.assertEqual(api_ref.h2["class"], "api_header")
        self.assertEqual(api_ref.h2.string, unicode("API Reference"))
# there are 3 top level comp groups
        component_groups = api_ref.findAll("div", recursive = False)
        self.assertEqual(len(component_groups), 3)
# 1) classes
        cg_classes = component_groups[0]
# there are 4 classes
        classes = self.check_cg_h3(cg_classes, "Classes", 4)

# class 1 is empty
        class1_subcomps = self.check_comp_h4(classes[0], "empty_class", 0)

# class 2 only has a single ctor
        class2_subcomps = self.check_comp_h4(classes[1], "only_one_ctor", 1)
        class2_ctors = self.check_cg_div(class2_subcomps[0], "Constructors", 1)
        class2_ctor_subcomps = \
            self.check_comp_div(class2_ctors[0], "only_one_ctor(options)", 1)

# class 3 has a ctor and a method
        class3_subcomps = self.check_comp_h4(classes[2], "ctor_and_method", 2)
        class3_ctors = self.check_cg_div(class3_subcomps[0], "Constructors", 1)
        class3_ctor_subcomps = \
            self.check_comp_div(class3_ctors[0], "ctor_and_method(options)", 1)
        class3_methods = self.check_cg_div(class3_subcomps[1], "Methods", 1)
        class3_method_subcomps = \
            self.check_comp_div(class3_methods[0], "a_method(options)", 1)

# class 4 has a property too
        class4_subcomps = \
            self.check_comp_h4(classes[3], "ctor_and_method_and_prop", 3)
        class4_ctors = self.check_cg_div(class4_subcomps[0], "Constructors", 1)
        class4_ctor_subcomps = \
            self.check_comp_div(class4_ctors[0], \
                                "ctor_and_method_and_prop(options)", 1)
        class4_methods = self.check_cg_div(class4_subcomps[1], "Methods", 1)
        class4_method_subcomps = \
            self.check_comp_div(class4_methods[0], "a_method(options)", 1)
        class4_props = self.check_cg_div(class4_subcomps[2], "Properties", 1)
        class4_prop_subcomps = \
            self.check_comp_div(class4_props[0], 'a_property : ', 0)

# 2) functions
        cg_functions = component_groups[1]
# there are 4 functions, too
        functions = self.check_cg_h3(cg_functions, "Functions", 4)
# function 1
# first subcomps is a parameter set containing 4 params
# second is a returns value
        function1_subcomps = \
            self.check_comp_h4(functions[0], \
                "test(argOne, argTwo, argThree=default, options)", 2)
        function1_params = \
            self.check_param_set(function1_subcomps[0], 4)
        self.check_returns(function1_subcomps[1])

# function 2
# has a single param and no returns
        function2_subcomps = \
            self.check_comp_h4(functions[1], "append(options)", 1)
        function2_params = \
            self.check_param_set(function2_subcomps[0], 1)

# function 3
# has 5 params and a return value
        function3_subcomps = \
            self.check_comp_h4(functions[2], \
                "cool_func(howMuch, double=true, options, onemore, options2)", 2)
        function3_params = \
            self.check_param_set(function3_subcomps[0], 5)
        self.check_returns(function3_subcomps[1])

# function 4
# has 0 params and a return value
        function4_subcomps = \
            self.check_comp_h4(functions[3], "random()", 1)
        self.check_returns(function4_subcomps[0])

# 3) Properties
        cg_properties = component_groups[2]
# there is 1 property
        properties = self.check_cg_h3(cg_properties, "Properties", 1)
        self.check_comp_h4(properties[0], "test_property : ", 0)

# a pile of helper functions
    def check_cg_h3(self, cg, cg_name, component_count):
        self.assertEqual(cg["class"], "api_component_group")
        self.assertEqual(cg.h3["class"], "api_header")
        self.assertEqual(cg.h3.string, unicode(cg_name))
        components = cg("div", recursive = False)
        self.assertEqual(len(components), component_count)
        return components

    def check_cg_div(self, cg, cg_name, component_count):
        self.assertEqual(cg["class"], "api_component_group")
        self.assertEqual(cg.div["class"], "api_header")
        self.assertEqual(cg.div.string, unicode(cg_name))
# -1 because the header is also a DIV
        components = cg("div", recursive = False)[1:]
        self.assertEqual(len(components), component_count)
        return components

    def check_comp_h4(self, comp, comp_name, sub_component_count):
        self.assertEqual(comp["class"], "api_component")
        self.assertEqual(comp.h4["class"], "api_name")
        self.assertEqual(comp.h4.contents[0], unicode(comp_name))
        sub_components = comp("div", recursive = False)
        self.assertEqual(len(sub_components), sub_component_count)
        return sub_components

    def check_comp_div(self, comp, comp_name, sub_component_count):
        self.assertEqual(comp["class"], "api_component")
        self.assertEqual(comp.div["class"], "api_name")
        self.assertEqual(comp.div.contents[0], unicode(comp_name))
# -1 because the header is also a DIV
        sub_components = comp("div", recursive = False)[1:]
        self.assertEqual(len(sub_components), sub_component_count)
        return sub_components

    def check_param_set(self, param_set, component_count):
        self.assertEqual(param_set["class"], "parameter_set")
        params = param_set("div", recursive = False)
        self.assertEqual(len(params), component_count)
        return params

    def check_returns(self, returns):
        self.assertEqual(returns["class"], "returns")
        self.assertEqual(returns.contents[0], unicode("Returns: "))


if __name__ == "__main__":
    unittest.main()
