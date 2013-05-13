# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import sys
import shutil
import hashlib
import tarfile
import StringIO

import apiparser
import apirenderer
import webdocs
from documentationitem import get_module_list
from documentationitem import get_devguide_list
from documentationitem import ModuleInfo
from documentationitem import DevGuideItemInfo
from linkrewriter import rewrite_links
import simplejson as json

DIGEST = "status.md5"
TGZ_FILENAME = "addon-sdk-docs.tgz"

def get_sdk_docs_path(env_root):
    return os.path.join(env_root, "doc")

def clean_generated_docs(docs_dir):
    status_file = os.path.join(docs_dir, "status.md5")
    if os.path.exists(status_file):
        os.remove(status_file)
    index_file = os.path.join(docs_dir, "index.html")
    if os.path.exists(index_file):
        os.remove(index_file)
    dev_guide_dir = os.path.join(docs_dir, "dev-guide")
    if os.path.exists(dev_guide_dir):
        shutil.rmtree(dev_guide_dir)
    api_doc_dir = os.path.join(docs_dir, "modules")
    if os.path.exists(api_doc_dir):
        shutil.rmtree(api_doc_dir)

def generate_docs(env_root, version):
    clean_generated_docs(get_sdk_docs_path(env_root))
    generate_docs_from_scratch(env_root, version)
    print "finished!"

def generate_named_file(env_root, filename_and_path):
    module_list = get_module_list(env_root)
    web_docs = webdocs.WebDocs(env_root, module_list, version)
    abs_path = os.path.abspath(filename_and_path)
    path, filename = os.path.split(abs_path)
    if abs_path.startswith(os.path.join(env_root, 'doc', 'module-source')):
        module_root = os.sep.join([env_root, "doc", "module-source"])
        module_info = ModuleInfo(env_root, module_root, path, filename)
        write_module_doc(env_root, web_docs, module_info, False)
    elif abs_path.startswith(os.path.join(get_sdk_docs_path(env_root), 'dev-guide-source')):
        devguide_root = os.sep.join([env_root, "doc", "dev-guide-source"])
        devguideitem_info = DevGuideItemInfo(env_root, devguide_root, path, filename)
        write_devguide_doc(env_root, web_docs, devguideitem_info, False)
    else:
        raise ValueError("Not a valid path to a documentation file")

def generate_docs_from_scratch(env_root, version):
    docs_dir = get_sdk_docs_path(env_root)
    module_list = get_module_list(env_root)
    web_docs = webdocs.WebDocs(env_root, module_list, version)
    clean_generated_docs(docs_dir)

    # py2.5 doesn't have ignore=, so we delete tempfiles afterwards. If we
    # required >=py2.6, we could use ignore=shutil.ignore_patterns("*~")
    for (dirpath, dirnames, filenames) in os.walk(docs_dir):
        for n in filenames:
            if n.endswith("~"):
                os.unlink(os.path.join(dirpath, n))

    # generate api docs for all modules
    if not os.path.exists(os.path.join(docs_dir, "modules")):
        os.mkdir(os.path.join(docs_dir, "modules"))
    [write_module_doc(env_root, web_docs, module_info) for module_info in module_list]

    # generate third-party module index
    third_party_index_file = os.sep.join([env_root, "doc", "module-source", "third-party-modules.md"])
    third_party_module_list = [module_info for module_info in module_list if module_info.level() == "third-party"]
    write_module_index(env_root, web_docs, third_party_index_file, third_party_module_list)

    # generate high-level module index
    high_level_index_file = os.sep.join([env_root, "doc", "module-source", "high-level-modules.md"])
    high_level_module_list = [module_info for module_info in module_list if module_info.level() == "high"]
    write_module_index(env_root, web_docs, high_level_index_file, high_level_module_list)

    # generate low-level module index
    low_level_index_file = os.sep.join([env_root, "doc", "module-source", "low-level-modules.md"])
    low_level_module_list = [module_info for module_info in module_list if module_info.level() == "low"]
    write_module_index(env_root, web_docs, low_level_index_file, low_level_module_list)

    # generate dev-guide docs
    devguide_list = get_devguide_list(env_root)
    [write_devguide_doc(env_root, web_docs, devguide_info) for devguide_info in devguide_list]

    # make /md/dev-guide/welcome.html the top level index file
    doc_html = web_docs.create_guide_page(os.path.join(docs_dir, 'dev-guide-source', 'index.md'))
    write_file(env_root, doc_html, docs_dir, 'index')

def write_module_index(env_root, web_docs, source_file, module_list):
    doc_html = web_docs.create_module_index(source_file, module_list)
    base_filename, extension = os.path.splitext(os.path.basename(source_file))
    destination_path = os.sep.join([env_root, "doc", "modules"])
    write_file(env_root, doc_html, destination_path, base_filename)

def write_module_doc(env_root, web_docs, module_info):
    doc_html = web_docs.create_module_page(module_info)
    write_file(env_root, doc_html, module_info.destination_path(), module_info.base_filename())

def write_devguide_doc(env_root, web_docs, devguide_info):
    doc_html = web_docs.create_guide_page(devguide_info.source_path_and_filename())
    write_file(env_root, doc_html, devguide_info.destination_path(), devguide_info.base_filename())

def write_file(env_root, doc_html, dest_dir, filename):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    dest_path_html = os.path.join(dest_dir, filename) + ".html"
    replace_file(env_root, dest_path_html, doc_html)
    return dest_path_html

def replace_file(env_root, dest_path, file_contents):
    if os.path.exists(dest_path):
        os.remove(dest_path)
    # before we copy the final version, we'll rewrite the links
    # I'll do this last, just because we know definitely what the dest_path is at this point
    if dest_path.endswith(".html"):
        file_contents = rewrite_links(env_root, get_sdk_docs_path(env_root), file_contents, dest_path)
    open(dest_path, "w").write(file_contents)

if __name__ == "__main__":
    if (len(sys.argv) < 3):
        print 'Usage: "generate.py <SDK_version> <full path to the SDK>'
        exit()
    version = sys.argv[1]
    env_root = sys.argv[2]
    if not os.path.isabs(env_root):
        print "Path to the SDK clone must be absolute"
        exit()
    generate_docs(env_root, version)
