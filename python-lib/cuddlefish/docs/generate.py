import os
import shutil
import hashlib
import tarfile

from cuddlefish import packaging
from cuddlefish import Bunch
from cuddlefish.docs import apiparser
from cuddlefish.docs import apirenderer
from cuddlefish.docs import webdocs
import simplejson as json

SDOCS_DIR = "addon-sdk-docs"
DIGEST = "status.md5"

def generate_static_docs(env_root, tgz_filename, base_url = ''):
    generate_docs(env_root, base_url)
    tgz = tarfile.open(tgz_filename, 'w:gz')
    tgz.add('addon-sdk-docs', 'addon-sdk-docs')
    tgz.close()

def generate_docs(env_root, base_url='', silent=False):
    sdocs_dir = os.path.join(env_root, SDOCS_DIR)
    if base_url == '':
        base_url_path = sdocs_dir
        # this is to ensure the path starts with "/"
        # whether or not it's on Windows
        # there might be a better way
        if not sdocs_dir.startswith("/"):
            base_url_path = "/" + base_url_path
        base_url_path_pieces = base_url_path.split(os.sep)
        base_url = "file://" + "/".join(base_url_path_pieces) + "/"
    # if the static docs dir doesn't exist, generate everything
    if not os.path.exists(sdocs_dir):
        if not silent:
            print "Generating documentation..."
        generate_docs_from_scratch(env_root, base_url)
        current_status = calculate_current_status(env_root)
        open(os.path.join(env_root, SDOCS_DIR, DIGEST), "w").write(current_status)
    else:
        current_status = calculate_current_status(env_root)
        previous_status_file = os.path.join(env_root, SDOCS_DIR, DIGEST)
        docs_are_up_to_date = False
        if os.path.exists(previous_status_file):
            docs_are_up_to_date = current_status == open(previous_status_file, "r").read()
        # if the docs are not up to date, generate everything
        if not docs_are_up_to_date:
            if not silent:
                print "Regenerating documentation..."
            shutil.rmtree(sdocs_dir)
            generate_docs_from_scratch(env_root, base_url)
            open(os.path.join(env_root, SDOCS_DIR, DIGEST), "w").write(current_status)
    return base_url + "index.html"

# this function builds a hash of the name and last modification date of:
# * every file in "packages" which ends in ".md"
# * every file in "static-files" which does not start with "."
def calculate_current_status(env_root):
    current_status = hashlib.md5()
    package_src_dir = os.path.join(env_root, "packages")
    for (dirpath, dirnames, filenames) in os.walk(package_src_dir):
        for filename in filenames:
            if filename.endswith(".md"):
                current_status.update(filename)
                current_status.update(str(os.path.getmtime(os.path.join(dirpath, filename))))
    guide_src_dir = os.path.join(env_root, "static-files")
    for (dirpath, dirnames, filenames) in os.walk(guide_src_dir):
        for filename in filenames:
            if not filename.startswith("."):
                current_status.update(filename)
                current_status.update(str(os.path.getmtime(os.path.join(dirpath, filename))))
    return current_status.digest()

def generate_docs_from_scratch(env_root, base_url):
    sdocs_dir = os.path.join(env_root, SDOCS_DIR)
    web_docs = webdocs.WebDocs(env_root, base_url)
    if os.path.exists(sdocs_dir):
        shutil.rmtree(sdocs_dir)

    # first, copy static-files
    shutil.copytree(os.path.join(env_root, 'static-files'), sdocs_dir)
    # py2.5 doesn't have ignore=, so we delete tempfiles afterwards. If we
    # required >=py2.6, we could use ignore=shutil.ignore_patterns("*~")
    for (dirpath, dirnames, filenames) in os.walk(sdocs_dir):
        for n in filenames:
            if n.endswith("~"):
                os.unlink(os.path.join(dirpath, n))

    # generate api docs from all packages
    os.mkdir(os.path.join(sdocs_dir, "packages"))
    # create the index file and save that
    pkg_cfg = packaging.build_pkg_cfg(env_root)
    index = json.dumps(packaging.build_pkg_index(pkg_cfg))
    index_path = os.path.join(sdocs_dir, "packages", 'index.json')
    open(index_path, 'w').write(index)

    # for each package, generate its docs
    for pkg_name, pkg in pkg_cfg['packages'].items():
        src_dir = pkg.root_dir
        dest_dir = os.path.join(sdocs_dir, "packages", pkg_name)
        os.mkdir(dest_dir)

        src_readme = os.path.join(src_dir, "README.md")
        if os.path.exists(src_readme):
            shutil.copyfile(src_readme,
                            os.path.join(dest_dir, "README.md"))

        # create the package page
        package_filename = os.path.join(dest_dir, pkg_name + ".html")
        if not os.path.exists(package_filename):
            package_doc_html = web_docs.create_package_page(src_dir)
            open(package_filename, "w").write(package_doc_html)

        # generate all the API docs
        docs_src_dir = os.path.join(src_dir, "doc")
        docs_dest_dir = os.path.join(dest_dir, "doc")
        if os.path.isdir(os.path.join(src_dir, "docs")):
            docs_src_dir = os.path.join(src_dir, "docs")
            docs_dest_dir = os.path.join(dest_dir, "docs")
        generate_file_tree(docs_src_dir, docs_dest_dir, web_docs, generate_api_doc)

    # generate all the guide docs
    dev_guide_src = os.path.join(env_root, 'static-files', 'md', 'dev-guide')
    dev_guide_dest = os.path.join(sdocs_dir, 'dev-guide')
    generate_file_tree(dev_guide_src, dev_guide_dest, web_docs, generate_guide_doc)

    # make /md/dev-guide/welcome.html the top level index file
    shutil.copy(os.path.join(dev_guide_dest, 'welcome.html'), \
                os.path.join(sdocs_dir, 'index.html'))

def generate_file_tree(src_dir, dest_dir, web_docs, generate_file):
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)
    for (dirpath, dirnames, filenames) in os.walk(src_dir):
        assert dirpath.startswith(src_dir) # what is this for??
        relpath = dirpath[len(src_dir) + 1:]
        for dirname in dirnames:
            dest_path = os.path.join(dest_dir, relpath, dirname)
            if not os.path.exists(dest_path):
                os.mkdir(dest_path)
        for filename in filenames:
            if filename.endswith("~"):
                continue
            src_path = os.path.join(dirpath, filename)
            dest_path = os.path.join(dest_dir, relpath, filename)
            generate_file(src_path, dest_path, web_docs)

def generate_api_doc(src_dir, dest_dir, web_docs):
    shutil.copyfile(src_dir, dest_dir)
    if src_dir.endswith(".md"):
        # parse and JSONify the API docs
        docs_md = open(src_dir, 'r').read()
        docs_parsed = list(apiparser.parse_hunks(docs_md))
        docs_json = json.dumps(docs_parsed)
        open(dest_dir + ".json", "w").write(docs_json)
        # write the HTML div files
        docs_div = apirenderer.json_to_div(docs_parsed, src_dir)
        open(dest_dir + ".div", "w").write(docs_div)
        # write the standalone HTML files
        docs_html = web_docs.create_module_page(src_dir)
        open(dest_dir[:-3] + ".html", "w").write(docs_html)

def generate_guide_doc(src_dir, dest_dir, web_docs):
    if src_dir.endswith(".md"):
        # write the standalone HTML files
        docs_html = web_docs.create_guide_page(src_dir)
        open(dest_dir[:-3] + ".html", "w").write(docs_html)