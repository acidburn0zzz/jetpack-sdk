import sys, os
import markdown
import time

# list of all the 'class' and 'id' attributes assigned to
# <div> and <span> tags by the renderer.
API_REFERENCE = 'api_reference'
MODULE_API_DOCS_CLASS = 'module_api_docs'
MODULE_API_DOCS_ID = '_module_api_docs'
API_HEADER = 'api_header'
API_NAME = 'api_name'
API_COMPONENT_GROUP = 'api_component_group'
API_COMPONENT = 'api_component'
DATATYPE = 'datatype'
RETURNS = 'returns'
PARAMETER_SET = 'parameter_set'
MODULE_DESCRIPTION = 'module_description'

HTML_HEADER = '''
<!DOCTYPE html>\n
<html>\n
<head>\n
  <meta http-equiv="Content-type" content="text/html; charset=utf-8" />\n
  <base target="_blank"/>\n
  <link rel="stylesheet" type="text/css" media="all"\n
        href="../../../css/base.css" />\n
  <link rel="stylesheet" type="text/css" media="all"\n
        href="../../../css/apidocs.css" />\n
  <title>Add-on SDK Documentation</title>\n
  <style type="text/css">\n
    body {\n
      border: 50px solid #FFFFFF;\n
    }\n
  </style>\n
\n
  <script type="text/javascript">\n
    function rewrite_links() {\n
      var images = document.getElementsByTagName("img");\n
      for (var i = 0; i < images.length; i++) {\n
        var before = images[i].src.split("packages/")[0];\n
        var after = images[i].src.split("/docs")[1];\n
        images[i].src = before + after;\n
      }\n
    }\n
    </script>\n
</head>\n
\n
<body onload = "rewrite_links()">\n'''

HTML_FOOTER = '''
</body>\n
\n
</html>\n'''

def indent(text_in):
    text_out = ''
    lines = text_in.splitlines(True)
    indentation_level = 0
    indentation_depth = 2
    for line in lines:
        if (line.startswith('<div')):
            text_out += ((' ' * indentation_depth) * indentation_level) + line
            if not '</div>' in line:
                indentation_level += 1
        else:
            if (line.startswith('</div>')):
                indentation_level -= 1
            text_out += ((' ' * indentation_depth) * indentation_level) + line
    return text_out

def tag_wrap_id(text, classname, id, tag = 'div'):
    return ''.join(['\n<'+ tag + ' id="', id, '" class="', \
                   classname, '">\n', text + '\n</' + tag +'>\n'])

def tag_wrap(text, classname, tag = 'div'):
    return ''.join(['\n<' + tag + ' class="', classname, '">', \
                   text, '\n</'+ tag + '>\n'])

def tag_wrap_inline(text, classname, tag = 'div'):
    return ''.join(['\n<' + tag + ' class="', classname, '">', \
                   text, '</'+ tag + '>\n'])

def span_wrap(text, classname):
    return ''.join(['<span class="', classname, '">', \
                   text, '</span>'])

class API_Renderer(object):
    def __init__(self, json, tag):
        self.name = json['name']
        self.tag = tag
        self.description = json.get('desc', '')
        self.json = json

    def render_name(self):
        raise Exception('not implemented in this class')

    def render_description(self):
        return markdown.markdown(self.description)

    def render_subcomponents(self):
        raise Exception('not implemented in this class')

    def get_tag(self):
        return self.tag

class Class_Doc(API_Renderer):
    def __init__(self, json, tag):
        API_Renderer.__init__(self, json, tag)

    def render_name(self):
        return self.name

    def render_subcomponents(self):
        return render_object_contents(self.json)

class Function_Doc(API_Renderer):
    def __init__(self, json, tag, owner=None):
        API_Renderer.__init__(self, json, tag)
        self.owner = owner
        self.returns = json.get('returns', None)
        self.parameters_json = json.get('params', None)
        self.signature = self._assemble_signature()

    def render_name(self):
        if (self.owner):
            return self.owner + '.' + self.signature
        else:
            return self.signature

    def render_subcomponents(self):
        return self._render_parameters() + self._render_returns()

    def _render_parameters(self):
        if  not self.parameters_json:
            return ''
        text = ''.join([render_comp(Parameter_Doc(parameter_json, 'div')) \
                       for parameter_json in self.parameters_json])
        return tag_wrap(text, PARAMETER_SET)

    def _render_returns(self):
        if not self.returns:
            return ''
        text = 'Returns: ' + span_wrap(self.returns['type'], DATATYPE)
        if "desc" in self.returns:
            text += markdown.markdown(self.returns['desc'])
        return tag_wrap(text, RETURNS)

    def _assemble_signature(self):
        signature = self.name + "("
        if self.parameters_json and len(self.parameters_json) > 0:
            signature += self.parameters_json[0]["name"]
            for parameters_json in self.parameters_json[1:]:
                signature += ", " + parameters_json["name"]
        signature += ")"
        return signature

class Parameter_Doc(API_Renderer):
    def __init__(self, json, tag):
        API_Renderer.__init__(self, json, tag)
        self.datatype = json.get('type', None)
        self.properties_json = json.get('properties', None)

    def render_name(self):
        if self.datatype:
            return self.name + ' : ' + \
                   span_wrap(self.datatype, DATATYPE)
        return self.name

    def render_subcomponents(self):
        if not self.properties_json:
            return ''
        text = ''.join([render_comp(Property_Doc(property_json, 'div')) \
                       for property_json in self.properties_json])
        return text

class Property_Doc(API_Renderer):
    def __init__(self, json, tag, owner = None):
        API_Renderer.__init__(self, json, tag)
        self.owner = owner
        self.datatype = json['type']

    def render_name(self):
        if self.owner:
            rendered_name = self.owner + '.' + self.name
        else:
            rendered_name = self.name
        return rendered_name + ' : ' + \
               span_wrap(self.datatype, DATATYPE)

    def render_subcomponents(self):
        return render_object_contents(self.json)

def render_object_contents(json):
    ctor = json.get('constructor', None)
    text = ''
    if ctor:
        text += render_comp_group([ctor], 'Constructors', Function_Doc)
    methods = json.get('functions', None)
    text += render_comp_group(methods, 'Methods', Function_Doc)
    properties = json.get('properties', None)
    text += render_comp_group(properties, 'Properties', Property_Doc)
    return text

def render_comp(component):
    # a component is wrapped inside a single div marked 'API_COMPONENT'
    # containing:
    # 1) the component name, marked 'API_NAME'
    text = tag_wrap_inline(component.render_name(), \
                           API_NAME, component.get_tag())
    # 2) the component description
    text += component.render_description()
    # 3) the component contents
    text += component.render_subcomponents()
    return tag_wrap(text, API_COMPONENT)

def render_comp_group(group, group_name, ctor, tag = 'div', comp_tag = 'div'):
    if not group or len(group) == 0:
        return ''
    # component group is a list of components in a single div called
    # 'API_COMPONENT_GROUP' containing:
    # 1) a title for the group marked with 'API_HEADER'
    text = tag_wrap_inline(group_name, API_HEADER, tag)
    # 2) each component
    text += ''.join([render_comp(ctor(api, comp_tag)) for api in group])
    return tag_wrap(text, API_COMPONENT_GROUP)

def render_descriptions(descriptions_md):
    text = ''.join([description_md for description_md in descriptions_md])
    return tag_wrap(markdown.markdown(text), MODULE_DESCRIPTION)

def render_api_reference(api_docs):
    if (len(api_docs["classes"]) == 0) and \
       (len(api_docs["functions"]) == 0) and \
       (len(api_docs["properties"]) == 0):
        return ''
    # at the top level api reference is in a single div marked 'API_REFERENCE',
    # containing:
    # 1) a title 'API Reference' marked with 'API_HEADER'
    text = tag_wrap_inline('API Reference', API_HEADER, 'h2')
    # 2) a component group called 'Classes' containing any class elements
    text += render_comp_group(api_docs["classes"], \
                              'Classes', Class_Doc, 'h3', 'h4')
    # 3) a component group called 'Functions' containing any global functions
    text += render_comp_group(api_docs["functions"], \
                              'Functions', Function_Doc, 'h3', 'h4')
    # 4) a component group called 'Properties' containing any global properties
    text += render_comp_group(api_docs["properties"], \
                              'Properties', Property_Doc, 'h3', 'h4')
    return tag_wrap(text, API_REFERENCE)

def fix_constructor_names(json):
    classes = json["classes"]
    for class_json in classes:
        ctor = class_json.get("constructor", None)
        if ctor and "name" not in ctor:
            ctor["name"] = class_json["name"]
    return json

# take the JSON output of apiparser
# return the HTML DIV containing the rendered component
def json_to_div(json):
    json = fix_constructor_names(json)
    module_name = json.get("module", "")
    text = "<h1>" + module_name + "</h1>"
    text += tag_wrap(markdown.markdown(json["desc"]), MODULE_DESCRIPTION)
    text += render_api_reference(json)
    text = tag_wrap_id(text, MODULE_API_DOCS_CLASS, \
                       module_name + MODULE_API_DOCS_ID)
    return text.encode('utf8')

# take the JSON output of apiparser
# return standalone HTML containing the rendered component
def json_to_html(json):
    return indent(HTML_HEADER + \
           json_to_div(json) + HTML_FOOTER)

if __name__ == '__main__':
    if (len(sys.argv) == 0):
        print 'Supply the name of a docs file to parse'
    else:
        print json_to_html(sys.argv[1])
