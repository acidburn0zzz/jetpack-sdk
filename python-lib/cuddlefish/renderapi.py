import sys, os
import markdown
import apiparser
import time

# list of all the "class" and "id" attributes assigned to
# <div> and <span> tags by the renderer.
API_REFERENCE = "api_reference"
MODULE_API_DOCS_CLASS = "module_api_docs"
MODULE_API_DOCS_ID = "_module_api_docs"
API_HEADER = "api_header"
API_NAME = "api_name"
API_COMPONENT_GROUP = "api_component_group"
API_COMPONENT = "api_component"
DATATYPE = "datatype"
RETURNS = "returns"
PARAMETER_SET = "parameter_set"
MODULE_DESCRIPTION = "module_description"

# class attribute used to indicate an internal link that must
# be fixed up by some script in the front end
INTERNAL_LINK = "internal_link"

module_name = ""

def indent(text_in):
    text_out = ""
    lines = text_in.splitlines(True)
    indentation_level = 0
    indentation_depth = 2
    for line in lines:
        if (line.startswith("<div")):
            text_out += ((" " * indentation_depth) * indentation_level) + line
            indentation_level += 1
        else:
            if (line.startswith("</div>")):
                indentation_level -= 1
            text_out += ((" " * indentation_depth) * indentation_level) + line
    return text_out

def div_wrap_id(text, classname, id):
    div_tag = "\n<div id='" + id + "' class='" + classname + "'>\n"
    return div_tag + text + "\n</div>\n"

def div_wrap(text, classname):
    div_tag = "\n<div class='" + classname + "'>\n"
    return div_tag + text + "\n</div>\n"

def span_wrap(text, classname):
    span_tag = "<span class='" + classname + "'>"
    return span_tag + text + "</span>"

def render_description(text):
    return text

class API_Renderer(object):
    @staticmethod
    def create_renderer(json):
        for subclass in API_Renderer.__subclasses__():
            if subclass._is_renderer_for(json):
                return subclass(json)

    def __init__(self, json):
        self.name = json['name']
        self.description = json.get('description', "")

    def render(self):
        text = div_wrap(self._render_name(), API_NAME)
        text += render_description(self.description)
        text += self._render_subcomponents()
        return div_wrap(text, API_COMPONENT)

    def _render_name(self):
        raise Exception("not implemented in this class")

    def _render_subcomponents(self):
        raise Exception("not implemented in this class")

class ObjectContents_Doc():
    def __init__(self, json, owner):
        self.owner = owner 
        self.constructors_json = json.get('constructors', None)
        self.methods_json = json.get('methods', None)
        self.properties_json = json.get('properties', None)

    def render(self):
        text =  self._render_subcomponents(self.constructors_json, Function_Doc, "Constructors")
        text += self._render_subcomponents(self.methods_json, Function_Doc, "Methods")
        text += self._render_subcomponents(self.properties_json, Property_Doc, "Properties")
        return text

    def _render_subcomponents(self, components_json, ctor_function, title):
        if (not components_json):
            return ""
        text = div_wrap(title, API_HEADER)
        text += "".join([ctor_function(component_json).render() \
                       for component_json in components_json])
        return div_wrap(text, API_COMPONENT_GROUP)

class Class_Doc(API_Renderer):
    def __init__(self, json):
        API_Renderer.__init__(self, json)
        self.object_contents = ObjectContents_Doc(json, self.name)

    @classmethod
    def _is_renderer_for(self, json):
        return json['type'] == 'class'

    def _render_name(self):
        return self.name

    def _render_subcomponents(self):
        return self.object_contents.render()

class Function_Doc(API_Renderer):
    def __init__(self, json, owner=None):
        API_Renderer.__init__(self, json)
        self.owner = owner
        self.signature = json['signature']
        self.returns = json.get('returns', None)
        self.parameters_json = json.get('params', None)

    @classmethod
    def _is_renderer_for(self, json):
        return (json['type'] == 'function') or \
               (json['type'] == 'constructor') or \
               (json['type'] == 'method')

    def _render_name(self):
        if (self.owner):
            return self.owner + "." + self.signature
        else:
            return self.signature

    def _render_subcomponents(self):
        return self._render_parameters() + self._render_returns()

    def _render_parameters(self):
        if  not self.parameters_json:
            return ""
        text = "".join([Parameter_Doc(parameter_json).render() \
                       for parameter_json in self.parameters_json])
        return div_wrap(text, PARAMETER_SET)

    def _render_returns(self):
        if not self.returns:
            return ""
        text = "Returns: " + span_wrap(self.returns['datatype'], DATATYPE)
        text += render_description(self.returns['description'])
        return div_wrap(text, RETURNS)

class Parameter_Doc(API_Renderer):
    def __init__(self, json):
        API_Renderer.__init__(self, json)
        self.datatype = json['datatype']
        self.properties_json = json.get("props", None)

    @classmethod
    def _is_renderer_for(self, json):
        return json['type'] == 'parameter'

    def _render_name(self):
        return self.name + " : " + span_wrap(self.datatype, DATATYPE)

    def _render_subcomponents(self):
        if not self.properties_json:
            return ""
        text = "".join([Property_Doc(property_json).render() \
                       for property_json in self.properties_json])
        return text

class Property_Doc(API_Renderer):
    def __init__(self, json, owner = None):
        API_Renderer.__init__(self, json)
        self.owner = owner
        self.datatype = json['datatype']
        self.object_contents = ObjectContents_Doc(json, self.name)

    @classmethod
    def _is_renderer_for(self, json):
        return json['type'] == 'property'

    def _render_name(self):
        if self.owner:
            rendered_name = self.owner + "." + self.name
        else:
            rendered_name = self.name
        return rendered_name + " : " + span_wrap(self.datatype, DATATYPE)

    def _render_subcomponents(self):
        return self.object_contents.render()

def render_descriptions(descriptions_md):
    text = "".join([render_description(description_md) for description_md in descriptions_md])
    return div_wrap(text, MODULE_DESCRIPTION)

def render_group(apis_json, group_name, group_type):
    renderers = [API_Renderer.create_renderer(api_json) \
                for api_json in apis_json 
                if api_json['type'] == group_type]
    if len(renderers) == 0:
        return ""
    text = div_wrap(group_name, API_HEADER)
    text += "".join([renderer.render() for renderer in renderers])
    return div_wrap(text, API_COMPONENT_GROUP)

def render_api_reference(apis_json):
    text = div_wrap("API Reference", API_HEADER)
    text += render_group(apis_json, "Classes", "class")
    text += render_group(apis_json, "Functions", "function")
    text += render_group(apis_json, "Properties", "property")
    return div_wrap(text, API_REFERENCE)

def div(hunks, module_name):
    descriptions_md = [hunk[1] for hunk in hunks if hunk[0]=='markdown']
    api_docs_md = [hunk[1] for hunk in hunks if hunk[0]=='api-json']
    text = render_descriptions(descriptions_md)
    if (len(api_docs_md) > 0):
        text += render_api_reference(api_docs_md)
    return div_wrap_id(text, MODULE_API_DOCS_CLASS, module_name + MODULE_API_DOCS_ID)

def json_to_div(json, docs_md):
    root, ext = os.path.splitext(os.path.basename(docs_md))
    module_name = root
    print root
    div_text = div(json, module_name)
    div_text = markdown.markdown(div_text)
    return div_text.encode("utf8")

def json_to_html(json, docs_md):
    return json_to_div(json, docs_md)

def md_to_div(docs_md):
    docs_text = open(docs_md).read()
    hunks = list(apiparser.parse_hunks(docs_text))
    return json_to_html(hunks, docs_md)

def md_to_html(docs_md):
    return md_to_div(docs_md)

if __name__ == "__main__":
    if (len(sys.argv) == 0):
        print "Supply the name of a docs file to parse"
    else:
        print indent(md_to_html(sys.argv[1]))
