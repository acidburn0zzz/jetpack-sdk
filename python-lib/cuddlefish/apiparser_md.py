import sys, re, textwrap

VERSION = 3

class ParseError(Exception):
    # args[1] is the line number that caused the problem
    def __init__(self, why, lineno):
        self.why = why
        self.lineno = lineno
    def __str__(self):
        return ("ParseError: the JS API docs were unparseable on line %d: %s" %
                        (self.lineno, self.why))

class Accumulator:
    def __init__(self, holder, firstline):
        self.holder = holder
        self.firstline = firstline
        self.otherlines = []
    def addline(self, line):
        self.otherlines.append(line)
    def finish(self):
        # take a list of strings like:
        #    "initial stuff"    (this is in firstline)
        #    "  more stuff"     (this is in lines[0])
        #    "  yet more stuff"
        #    "      indented block"
        #    "      indented block"
        #    "  nonindented stuff"  (lines[-1])
        #
        # calculate the indentation level by looking at all but the first
        # line, and removing the whitespace they all have in common. Then
        # join the results with newlines and return a single string.
        pieces = []
        if self.firstline:
            pieces.append(self.firstline)
        if self.otherlines:
            pieces.append(textwrap.dedent("\n".join(self.otherlines)))
        self.holder["desc"] = "\n".join(pieces)


class APIParser:
    def parse(self, lines, lineno):
        api = {"line_number": lineno + 1}
# assign the name from the first line, of the form "<api name="API_NAME">"
        title_line = lines[lineno].rstrip("\n")
        api["name"] = self._parse_title_line(title_line, lineno + 1)
        lineno += 1
# finished with the first line, assigned the name
        working_set = self._initialize_working_set()
        props = []
        currentPropHolder = api
# fetch the next line, of the form "@tag [name] {datatype} description"
# and parse it into tag, info, description
        tag, info, firstline = parseTypeLine(lines[lineno], lineno + 1)
        api_type = tag
# if this API element is a property then datatype must be set
        if tag == 'property':
            api['type'] = info['type']
        # info is ignored
        currentAccumulator = Accumulator(api, firstline)
        lineno += 1
        while (lineno) < len(lines):
            line = lines[lineno].rstrip("\n")
            # accumulate any multiline descriptive text belonging to
            # the preceding "@" section
            if self._is_description_line(line):
                currentAccumulator.addline(line)
            else:
                currentAccumulator.finish()
                if line.startswith("<api"):
                # then we should recursively handle a nested element
                    nested_api, nested_api_type, lineno = self.parse(lines, lineno)
                    self._update_working_set(nested_api, nested_api_type, working_set)
                elif line.startswith("</api"):
                # then we have finished parsing this api element
                    currentAccumulator.finish()
                    if props and currentPropHolder:
                        currentPropHolder["properties"] = props
                    self._assemble_api_element(api, api_type, working_set)
                    return api, api_type, lineno
                else:
                # then we are looking at a subcomponent of an <api> element
                    tag, info, desc = parseTypeLine(line, lineno + 1)
                    currentAccumulator = Accumulator(info, desc)
                    if tag == "prop":
                        # build up props[]
                        props.append(info)
                    elif tag == "returns":
                        # close off the @prop list
                        if props and currentPropHolder:
                            currentPropHolder["properties"] = props
                            props = []
                        api["returns"] = info
                        currentPropHolder = info
                    elif tag == "param":
                        # close off the @prop list
                        if props and currentPropHolder:
                            currentPropHolder["properties"] = props
                            props = []
                        working_set["params"].append(info)
                        currentPropHolder = info
                    else:
                        raise ParseError("unknown '@' section header %s in \
                                           '%s'" % (tag, line), lineno + 1)
            lineno += 1
        raise ParseError("closing </api> tag not found", lineno + 1)

    def _parse_title_line(self, title_line, lineno):
        if "name" not in title_line:
            raise ParseError("Opening <api> tag must have a name attribute.",
                            lineno)
        m = re.search("name=['\"]{0,1}([-\w\.]*?)['\"]", title_line)
        if not m:
            raise ParseError("No value for name attribute found in "
                                     "opening <api> tag.", lineno)
        return m.group(1)

    def _is_description_line(self, line):
        return not ( (line.lstrip().startswith("@")) or
               (line.lstrip().startswith("<api")) or
               (line.lstrip().startswith("</api")) )

    def _initialize_working_set(self):
        # working_set accumulates api elements
        # that might belong to a parent api element
        working_set = {}
        working_set["constructor"] = []
        working_set["functions"] = []
        working_set["properties"] = []
        working_set["params"] = []
        return working_set

    def _update_working_set(self, nested_api, nested_api_type, working_set):
        # add this api element to whichever list is appropriate
        if nested_api_type == "constructor":
            if len(working_set["constructor"]) != 0:
                raise ParseError("class can only have one constructor", nested_api["line_number"])
            working_set["constructor"] = nested_api
        if nested_api_type == "method":
            working_set["functions"].append(nested_api)
        if nested_api_type == "property":
            working_set["properties"].append(nested_api)

    def _assemble_signature(self, api_element, params):
        signature = api_element["name"] + "("
        if len(params) > 0:
            signature += params[0]["name"]
            for param in params[1:]:
                signature += ", " + param["name"]
        signature += ")"
        api_element["signature"] = signature

    def _assemble_api_element(self, api_element, api_type, working_set):
        # if any of this working set's lists are non-empty,
        # add it to the current api element
        if (api_type == "constructor") or \
           (api_type == "function") or \
           (api_type == "method"):
           self._assemble_signature(api_element, working_set["params"])
        if len(working_set["params"]) > 0:
            api_element["params"] = working_set["params"]
        if len(working_set["properties"]) > 0:
            api_element["properties"] = working_set["properties"]
        if len(working_set["constructor"]) > 0:
            api_element["constructor"] = working_set["constructor"]
        if len(working_set["functions"]) > 0:
            api_element["functions"] = working_set["functions"]

def validate_info(tag, info, line, lineno):
    if tag == 'property':
        if not 'type' in info:
            raise ParseError("No type found for @property.", lineno)
    elif tag == "prop":
        if "type" not in info:
            raise ParseError("@prop lines must include {type}: '%s'" %
                              line, lineno)
        if "name" not in info:
            raise ParseError("@prop lines must provide a name: '%s'" %
                              line, lineno)

def parseTypeLine(line, lineno):
    # handle these things:
    #    @method
    #    @returns description
    #    @returns {string} description
    #    @param NAME {type} description
    #    @param NAME
    #    @prop NAME {type} description
    #    @prop NAME
    # returns:
    #    tag: type of api element
    #    info: linenumber, required, default, name, datatype
    #    description

    info = {"line_number": lineno}
    line = line.rstrip("\n")
    pieces = line.split()

    if not pieces:
        raise ParseError("line is too short: '%s'" % line, lineno)
    if not pieces[0].startswith("@"):
        raise ParseError("type line should start with @: '%s'" % line,
                             lineno)
    tag = pieces[0][1:]
    next_piece_index = 1

    expect_name = tag in ("param", "prop")

    if len(pieces) == 1:
        description = ""
    else:
        if pieces[next_piece_index].startswith("{"):
            # NAME is missing, pieces[1] is TYPE
            pass
        else:
            if expect_name:
                info["name"] = pieces[next_piece_index]
                next_piece_index += 1

        if len(pieces) > next_piece_index and pieces[next_piece_index].startswith("{"):
            info["type"] = pieces[next_piece_index].strip("{ }")
            next_piece_index += 1

        # we've got the metadata, now extract the description
        pieces = line.split(None, next_piece_index)
        if len(pieces) > next_piece_index:
            description = pieces[next_piece_index]
        else:
            description = ""
    validate_info(tag, info, line, lineno)
    return tag, info, description

def parse_api_doc(text):
    lines = text.splitlines(True)
    line_number = 0;
    description = ""
    module_json = {"version" : VERSION, \
                   "classes" : [], \
                   "functions" : [], \
                   "properties" : [], \
                   "desc" : ""}
    while line_number < len(lines):
        line = lines[line_number]
        if line.startswith("<api"):
            break
        module_json["desc"] += lines[line_number]
        line_number = line_number + 1
    while line_number < len(lines):
        if not lines[line_number].startswith("<api"):
            line_number = line_number + 1
            continue
        api_item, api_type, line_number = APIParser().parse(lines, line_number)
        if api_type == "class":
            module_json["classes"].append(api_item)
        elif api_type == "function":
            module_json["functions"].append(api_item)
        elif api_type == "property":
            module_json["properties"].append(api_item)
    return module_json

if __name__ == "__main__":
    json = False
    if sys.argv[1] == "--json":
        json = True
        del sys.argv[1]
    docs_text = open(sys.argv[1]).read()
    docs_parsed = parse_api_doc(docs_text)
    if json:
        import simplejson
        print simplejson.dumps(docs_parsed, indent=2)

