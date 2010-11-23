import sys, os
import markdown
import apiparser

markdowner = markdown.Markdown()

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
#should assert indent-level >=0
            text_out += ((" " * indentation_depth) * indentation_level) + line
    return text_out

def div_wrap_id(text, classname, id):
    div_tag = "<div id='" + id + "' class='" + classname + "'>"
    return div_tag + text + "</div>"

def div_wrap(text, classname):
    div_tag = "<div class='" + classname + "'>"
    return div_tag + text + "</div>"

def span_wrap(text, classname):
    span_tag = "<span class='" + classname + "'>"
    return span_tag + text + "</span>"

def renderDescription(text):
    return markdowner.convert(text)[:-1]

class API_Doc:
    def __init__(self, json):
        self.name = json['name']
        self.description = json.get('description', "")

    def render(self):
        text = span_wrap(self._renderName(), 'api-name')
        text += self._renderSubcomponents()
        text += renderDescription(text)
        return div_wrap(text, 'api_component')

    def _renderName(self):
        raise Exception("not implemented in this class")

    def _renderSubcomponents(self):
        raise Exception("not implemented in this class")

class ObjectContents_Doc():
    def __init__(self, json, owner):
        self.constructors = []
        self.methods = []
        self.properties = []
        self.owner = owner 
        constructors_json = json.get('constructors', None)
        if (constructors_json):
            for constructor_json in constructors_json:
                self.constructors.append(Function_Doc(constructor_json, self.owner))
        methods_json = json.get('methods', None)
        if (methods_json):
            for method_json in methods_json:
                self.methods.append(Function_Doc(method_json, self.owner))
        properties_json = json.get('properties', None)
        if (properties_json):
            for property_json in properties_json:
                self.properties.append(Property_Doc(property_json, self.owner))

    def render(self):
        text =  self._renderSubcomponentSet(self.constructors, "Constructors")
        text += self._renderSubcomponentSet(self.methods, "Methods")
        text += self._renderSubcomponentSet(self.properties, "Properties")
        return text

    def _renderSubcomponentSet(self, subcomponents, title):
        if (len(subcomponents) > 0):
            text = div_wrap(title, "api_header")
            for subcomponent in subcomponents:
                text += subcomponent.render()
            return div_wrap(text, "api_component_group")
        return ''

class Class_Doc(API_Doc):
    def __init__(self, json):
        API_Doc.__init__(self, json)
        self.object_contents = ObjectContents_Doc(json, self.name)
                
    def _renderName(self):
        return self.name

    def _renderSubcomponents(self):
        return self.object_contents.render()

class Function_Doc(API_Doc):
    def __init__(self, json, owner=None):
        API_Doc.__init__(self, json)
        self.owner = owner
        self.signature = json['signature']
        self.returns = json.get('returns', None)
        self.parameters = []
        params_json = json.get('params', None)
        if (params_json):
            for param_json in params_json:
                self.parameters.append(Parameter_Doc(param_json))

    def _renderName(self):
        if (self.owner):
            return self.owner + "." + self.signature
        else:
            return self.signature

    def _renderSubcomponents(self):
        return self._renderParameters() + self._renderReturns()

    def _renderParameters(self):
        text = ""
        for parameter in self.parameters:
            text += parameter.render()
        return div_wrap(text, "parameter_set")

    def _renderReturns(self):
        if (not self.returns):
            return ""
        text = "Returns: " + span_wrap(self.returns['type'], "property_type")
        text += renderDescription(self.returns['description'])
        return div_wrap(text, "returns")

class Parameter_Doc(API_Doc):
    def __init__(self, json):
        API_Doc.__init__(self, json)
        self.datatype = json['type']
        self.props = []
        props_json = json.get("props", None)
        if (props_json):
            for prop_json in props_json:
                self.props.append(Property_Doc(prop_json))

    def _renderName(self):
        return self.name + " : " + span_wrap(self.datatype, "data_type")

    def _renderSubcomponents(self):
        text = ""
        for prop in self.props:
            text += prop.render()
        return text

class Property_Doc(API_Doc):
    def __init__(self, json, owner = None):
        API_Doc.__init__(self, json)
        self.owner = owner
        self.datatype = json.get('property_type', 'type')
        self.object_contents = ObjectContents_Doc(json, self.name)

    def _renderName(self):
        if self.owner:
            renderedName = self.owner + "." + self.name
        else:
            renderedName = self.name
        return renderedName + " : " + span_wrap(self.datatype, "data_type")

    def _renderSubcomponents(self):
        return self.object_contents.render()

def renderAPIComponentGroup(component_group, title):
    text = span_wrap(title, "api-header")
    for component_doc in component_group:
        text += component_doc.render()
    return div_wrap(text, "api_component_group")

def renderDescriptions(descriptions_md):
    text = ""
    for description_md in descriptions_md:
        text += renderDescription(description_md)
    return div_wrap(text, "module_description")

def renderAPIReference(classes, functions, properties):
    text = div_wrap("API Reference", "api_header1")
    if (len(classes) > 0):
        text += renderAPIComponentGroup(classes, "Classes")
    if (len(functions) > 0):
        text += renderAPIComponentGroup(functions, "Functions")
    if (len(properties) > 0):
        text += renderAPIComponentGroup(properties, "Properties")
    return div_wrap(text, "api_reference")

def div(hunks, module_name):
    descriptions_md = []
    classes = []
    functions = []
    properties = []
    api_exists = False
    for h in hunks:
        if h[0] == 'markdown':
            descriptions_md.append(h[1])
        elif h[0] == 'api-json':
            api_exists = True
            entity = h[1]
            if entity['type'] == 'class':
                classes.append(Class_Doc(entity))
            elif entity['type'] == 'function':
                functions.append(Function_Doc(entity))
            elif entity['type'] == 'property':
                properties.append(Property_Doc(entity))

    text = renderDescriptions(descriptions_md)
    if (api_exists):
        text += renderAPIReference(classes, functions, properties)
    return div_wrap_id(text, 'module_api_docs', module_name + '_module_api_docs')

def render(docs_md):
    docs_text = open(docs_md).read()
    hunks = apiparser.parse_hunks(docs_text)
    root, ext = os.path.splitext(os.path.basename(sys.argv[1]))
    div_text =  indent(div(hunks, root))
#    md =  div_wrap(markdowner.convert("the ***word*** is: `try me`"), "try-me")
    return div_text.encode("utf8")

if __name__ == "__main__":
    if (len(sys.argv) == 0):
        print "Supply the name of a docs file to parse"
    else:    
        print(render(sys.argv[1]))

