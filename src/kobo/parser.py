import markdown
import datetime
import bs4
import os
from .helper import smart_capitalize, read
import json

md_extensions = [
    'meta',
    'def_list',
    'admonition',
    'toc',
    'markdown_katex'
]

md_extension_configs = {
}

md_css_classes = {
    'a': ['md-link'],
    'p': ['md-p'],
    'h1': ['md-header1']
}

admonition_types = [
    'definition',
    'theorem'
]

def parse_tree_save(contents_path, target_path=None):
    if not target_path:
        target_path = os.path.join(contents_path, '..', 'routes-freeze.json')
    write_tree = parse_tree(contents_path, write=True)
    tuple_to_dict = lambda route, html_path, title, template: {'route': route, 'html_path': html_path, 'title': title, 'template': template}
    routes_frozen = json.dumps([tuple_to_dict(*t) for t in write_tree])
    with open(target_path, 'w') as f:
        f.write(routes_frozen)

def parse_tree_load(frozen_path):
    with open(frozen_path) as f:
        routes_frozen = json.loads(f.read())
    dict_to_tuple = lambda entry: (entry.get('route'), read(entry.get('html_path')), entry.get('title'), entry.get('template'))
    return [dict_to_tuple(entry) for entry in routes_frozen]

def parse_tree(contents_path, write=False):
    '''Outputs a list of (route, html, title, template)'''
    tree = []
    if write:
        write_tree = []
    for root, dirs, files in os.walk(contents_path):
        root_routes = []
        for file in files:
            if file == 'index-blurb.md':
                continue
            if file.endswith('.md'): # only parse mds!
                (html, title, isdraft, route, template) = parse(os.path.join(root, file))
                html_path = os.path.join(root, file).replace('.md', '.html')

                if not route:
                    if file == 'index.md': # index -> parent dir should be the endpoint
                        route = os.path.relpath(root, contents_path)
                        if route == '.':
                            route = '/'
                    else:
                        relpath = os.path.relpath(os.path.join(root, file), contents_path) #gets the "effective path"
                        route = '/' + relpath[:-3] # strip off the .md at the end
                if not template:
                    if file == 'index.md':
                        template = 'index.html'
                    else:
                        template = 'page.html'
                if not isdraft:
                    root_routes.append((route, html, title, template))
                    if write:
                        with open(html_path, 'w') as f:
                            f.write(html)
                        write_tree.append((route, html_path, title, template))

        if 'index.md' not in files:
            # Add in an index

            route = '/' + os.path.relpath(root, contents_path)
            if 'index-blurb.md' in files:
                blurb_html, html = generate_index(root_routes, blurb_path=os.path.join(root, 'index-blurb.md'))
            else:
                blurb_html, html = generate_index(root_routes)
            title = 'index'
            template = 'index-list.html'
            root_routes.append((route, html, title, template))
            html_path = os.path.join(root, 'index.html')
            if write:
                with open(html_path, 'w') as f:
                    f.write(html)
                write_tree.append((route, html_path, title, template))
        tree.extend(root_routes)
    if write:
        return write_tree
    return tree

def generate_index(routes, blurb_path=None):
    index_md_atom = '- [%s](%s)'
    atoms = [index_md_atom % (title, route) for (route, html, title, template) in routes]
    index_md = '\n'.join(atoms)
    index_html, _, _, _, _ = __parse(index_md)
    if blurb_path:
        with open(blurb_path) as f:
            blurb_md = f.read()
        blurb_html, _, _, _, _ = __parse(blurb_md)
    else:
        blurb_html = ''

    return (blurb_html, index_html)

def parse(path, classes=md_css_classes):
    with open(path) as f:
        data = f.read()
    return __parse(data, classes=classes)

def __parse(data, classes=md_css_classes):
    md = markdown.Markdown(extensions=md_extensions, extension_configs=md_extension_configs)
    raw_html = md.convert(data)

    metadata = md.Meta
    isdraft = (metadata.get('draft', ['true']) == ['true'])
    title = metadata.get('title', [None])[0]
    route = metadata.get('route', [None])[0]
    template = metadata.get('template', [None])[0]

    soup = bs4.BeautifulSoup(raw_html)
    soup = apply_css_rules(soup, classes)
    soup = admonition_fix(soup)
    soup = image_alt_hover(soup)
    postprocessed_html = str(soup)

    return (postprocessed_html, title, isdraft, route, template)

def apply_css_rules(soup, css_classes):
    for tagtype in css_classes.keys():
        tags = soup.find_all(tagtype)
        for tag in tags:
            if tag.get('class'):
                tag['class'].extend(css_classes[tagtype])
            else:
                tag['class'] = css_classes[tagtype]
    return soup

def admonition_fix(soup):
    all_admonitions = soup.find_all('div', class_='admonition')
    for admonition in all_admonitions:
        admonition_type_list = list(set(admonition_types) & set(admonition['class']))
        if len(admonition_type_list):
            admonition_type = admonition_type_list[0]
            title_tag = admonition.find('p', class_='admonition-title')
            title = str(title_tag.string)
            if title.lower != admonition_type.replace('-', ' '):
                capitalized_admonition_type = admonition_type.replace('-', ' ').capitalize()
                new_title = smart_capitalize('%s: %s' % (capitalized_admonition_type, title))
                title_tag.string = new_title
        elif 'grid' in admonition['class']:
            title_tag = admonition.find('p', class_='admonition-title')
            title = str(title_tag.string)
            admonition['class'].append('grid-%s' % title)
            title_tag.decompose()
    return soup

def image_alt_hover(soup):
    for image_tag in soup.find_all('img', alt=True):
        if not image_tag.has_attr('title'):
            image_tag['title'] = image_tag['alt']
    return soup
