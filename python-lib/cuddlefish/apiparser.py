import os, sys, apiparser_md, docstract

def api_json_exists(module_json):
    return len(module_json["classes"]) != 0 or \
           len(module_json["functions"]) != 0 or \
           len(module_json["properties"]) != 0

def get_api_json(root, package_name, module_name):
    module_path = os.path.join(*module_name) + '.md'
    md_path = os.path.join(root, 'packages', package_name, 'docs', module_path)
    module_json = {}
    module_json["desc"] = ""
    module_json["classes"] = []
    module_json["functions"] = []
    module_json["properties"] = []

    module_json_js = None
    description_needed = True
    api_docs_needed = True

    if os.path.exists(md_path):
        # if the MD file exists at all, then use it for the
        # description (even if it's empty)
        description_needed = False
        module_json = apiparser_md.extractFromFile(md_path)
        api_docs_needed = not api_json_exists(module_json)

    if description_needed or api_docs_needed:
        try:
            m_path = os.path.join(*module_name) + '.js'
            js_path = \
                os.path.join(root, 'packages', package_name, 'lib', m_path)
            module_json_js = docstract.DocStract().extractFromFile(js_path)

        except:
            pass
            # if the js contains comments that use '/**' style, but aren't
            # formatted like dostract comments, gracefully ignore them
            # if would be nice here to use a specific exception for this
            # but docstract only raises a generic exception at present

    if description_needed and module_json_js and "desc" in module_json_js:
        module_json["desc"] = module_json_js["desc"]

    if api_docs_needed and module_json_js:
        if "classes" in module_json_js:
            module_json["classes"] = module_json_js["classes"]
        if "functions" in module_json_js:
            module_json["functions"] = module_json_js["functions"]
        if "properties" in module_json_js:
            module_json["properties"] = module_json_js["properties"]

    return module_json

if __name__ == "__main__":
    json = False
    if sys.argv[1] == "--json":
        json = True
        del sys.argv[1]
    docs_parsed = get_api_json(sys.argv[1], sys.argv[2])
    if json:
        import simplejson
        print simplejson.dumps(docs_parsed, indent = 2)
