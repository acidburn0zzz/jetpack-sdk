import sys, os
import markdown
import copy
import simplejson as json
# import apiparser
# import packageparser

from cuddlefish import packaging
from cuddlefish import Bunch
from cuddlefish import apiparser
from cuddlefish import apirenderer

INDEX_PAGE = '/static-files/index.html'
HIGH_LEVEL_PACKAGE_SUMMARIES = '<li id="high-level-package-summaries">'
LOW_LEVEL_PACKAGE_SUMMARIES = '<li id="low-level-package-summaries">'
CONTENT_ID = '<div id="right-column">'

def _get_files_in_dir(path):
    data = {}
    files = os.listdir(path)
    for filename in files:
        fullpath = os.path.join(path, filename)
        if os.path.isdir(fullpath):
            data[filename] = _get_files_in_dir(fullpath)
        else:
            try:
                info = os.stat(fullpath)
                data[filename] = dict(size=info.st_size)
            except OSError:
                pass
    return data

def build_pkg_index(pkg_cfg):
    pkg_cfg = copy.deepcopy(pkg_cfg)
    for pkg in pkg_cfg.packages:
        root_dir = pkg_cfg.packages[pkg].root_dir
        files = _get_files_in_dir(root_dir)
        pkg_cfg.packages[pkg].files = files
        try:
            readme = open(root_dir + '/README.md').read()
            pkg_cfg.packages[pkg].readme = readme
        except IOError:
            pass
        del pkg_cfg.packages[pkg].root_dir
    return pkg_cfg.packages

def build_pkg_cfg(root):
    pkg_cfg = packaging.build_config(root,
                                     Bunch(name='dummy'))
    del pkg_cfg.packages['dummy']
    return pkg_cfg

def get_modules(modules_json):
    modules = []
    for module in modules_json:
        if '.js' in module:
            modules.append(module[:-3])
        else:
            sub_modules = get_modules(modules_json[module])
            for sub_module in sub_modules:
                modules.append(module + '/' + sub_module)
    return modules

def tag_wrap(text, tag, attributes={}):
    result = ''
    result += '\n<' + tag
    for name in attributes.keys():
        result += ' ' + name + '=' + '"' + attributes[name] + '"'
    result +='>' + text + '</'+ tag + '>\n'
    return result

def create_module_list(package_json):
    package_name = package_json['name']
    modules = get_modules(package_json['files']['lib'])
    module_items = ''
    for module in modules:
        module_link = tag_wrap(module, 'a', {'href':'/packages/' + package_name + '/docs/' + module + '.html', 'target':'_self'})
        module_items += tag_wrap(module_link, 'li', {'class':'module'})
    return tag_wrap(module_items, 'ul', {'class':'modules'})

def create_package_summaries(packages_json, include):
    packages = ''
    for package_name in packages_json.keys():
        package_json = packages_json[package_name]
        if not include(package_json):
            continue
        package_link = tag_wrap(package_name, 'a', {'href':'/packages/'+ package_name + '.html', 'target':'_self'})
        text = tag_wrap(package_link, 'h4')
        text += create_module_list(package_json)
        packages += tag_wrap(text, 'div', {'class':'package-summary', 'style':'display: block;'})
    return packages

def is_high_level(package_json):
    return not is_low_level(package_json)

def is_low_level(package_json):
    return 'jetpack-low-level' in package_json['keywords']

def insert_after(target, insertion_point_id, text_to_insert):
    insertion_point = target.find(insertion_point_id) + len(insertion_point_id)
    return target[:insertion_point] + text_to_insert + target[insertion_point:]

def create_index_page(root):
    pkg_cfg = build_pkg_cfg(root)
    packages_json = build_pkg_index(pkg_cfg)
    index_page = open(root + INDEX_PAGE, 'r').read()
    high_level_summaries = create_package_summaries(packages_json, is_high_level)
    index_page = insert_after(index_page, HIGH_LEVEL_PACKAGE_SUMMARIES, high_level_summaries)
    low_level_summaries = create_package_summaries(packages_json, is_low_level)
    index_page = insert_after(index_page, LOW_LEVEL_PACKAGE_SUMMARIES, low_level_summaries)
    return index_page

def create_package_detail_row(package_json, field_descriptor, field_name):
    meta = tag_wrap(tag_wrap(field_descriptor, 'span', {'class':'meta-header'}), 'td')
    value = tag_wrap(tag_wrap(package_json[field_name], 'span', {'class':field_name}), 'td')
    return tag_wrap(meta + value, 'tr')

def create_package_detail_table(package_json):
    table_contents = create_package_detail_row(package_json, 'Author', 'author')
    print '1'
    table_contents += create_package_detail_row(package_json, 'Version', 'version')
    print '2'
    table_contents += create_package_detail_row(package_json, 'License', 'license')
    print '3'
#    table_contents += create_package_detail_row(package_json, 'Dependencies', 'dependencies')
    print '4'
    modules_meta = tag_wrap(tag_wrap('Modules', 'span', {'class':'meta-header'}), 'td')
    print '5'
    modules_value = tag_wrap(create_module_list(package_json), 'td')
    print '6'
    table_contents += tag_wrap(modules_meta + modules_value, 'tr')
    print '7'
    table = tag_wrap(tag_wrap(table_contents, 'tbody'), 'table', {'class':'meat-table'})
    return table

def create_package_detail(root, package_name):
    pkg_cfg = build_pkg_cfg(root)
    packages_json = build_pkg_index(pkg_cfg)
    package_json = packages_json[package_name]
    # pieces of the package detail
    package_title = tag_wrap(tag_wrap(package_name, 'span', {'class':'name'}), 'h1')
    table = create_package_detail_table(package_json)
    description = tag_wrap(tag_wrap(markdown.markdown(package_json['readme']), 'p'), 'div', {'class':'docs'})
    return tag_wrap(package_title + table + description, 'div', {'class':'package-detail'})

def create_guide_page(root, path):
    path, ext = os.path.splitext(path)
    md_path = path + '.md'
    guide_page = create_index_page(root)
    guide_content = markdown.markdown(open(md_path, 'r').read())
    guide_page = insert_after(guide_page, CONTENT_ID, guide_content)
    return guide_page.encode('utf8')

def create_module_page(root, path):
    path, ext = os.path.splitext(path)
    md_path = path + '.md'
    module_page = create_index_page(root)
    module_content = apirenderer.md_to_div(md_path)
    module_page = insert_after(module_page, CONTENT_ID, module_content)
    return module_page.encode('utf8')

def create_package_page(root, path):
    print path
    path, ext = os.path.splitext(path)
    package_name = path.split('/')[-1]
    print package_name
    package_page = create_index_page(root)
    package_content = create_package_detail(root, package_name)
    package_page = insert_after(package_page, CONTENT_ID, package_content)
    return package_page.encode('utf8')

# def create_module_page():

# def create_package_page():

if __name__ == '__main__':
    if (len(sys.argv) == 0):
        print 'Supply the name of a docs file to parse'
    else:
        pkg_cfg = build_pkg_cfg(sys.argv[1])
        packages_json = build_pkg_index(pkg_cfg)
        print(create_package_summaries(packages_json, is_low_level, 'high-level-package-summaries'))

