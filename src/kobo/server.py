from flask import Flask, render_template, url_for, redirect
from flask.views import View
from . import parser
from . import redirects
import os

DEBUG=False

class MarkdownView(View):
    def __init__(self, html, template, title):
        self.html = html
        self.template = template
        self.title = title
    def dispatch_request(self):
        return render_template(self.template, md_parsed=self.html, title=self.title)

class RedirectView(View):
    def __init__(self, target):
        self.target_url = target
    def dispatch_request(self):
        return redirect(self.target_url)

def create_server(root_directory, **kwargs):
    template_folder = root_directory / 'templates'
    static_folder = root_directory / 'static'
    contents_folder = root_directory / 'contents'
    redirects_path = root_directory / 'redirects.txt'
    frozen_path = root_directory / 'routes-freeze.json'
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)

    default_title = kwargs.get('default_title', 'my-site')
    write = kwargs.get('write', False)
    load_from_frozen = kwargs.get('load_from_frozen', False)
    if load_from_frozen == True:
        load_from_frozen = frozen_path

    def route_to_funcname(route):
        return route.replace('/', '_').replace('-', '_')

    if load_from_frozen:
        tree = parser.parse_tree_load(load_from_frozen)
    else:
        if write:
            tree = parser.parse_tree(contents_folder, write=True)
        else:
            tree = parser.parse_tree(contents_folder) # Outputs a list of routes and their paired html

    for route, html, title, template in tree:
        if DEBUG:
            print('Route %s (%s): %s' % (route, title, template))
        if title:
            app.add_url_rule(route, view_func=MarkdownView.as_view(route_to_funcname(route), html, template, title=title))
        else:
            app.add_url_rule(route, view_func=MarkdownView.as_view(route_to_funcname(route), html, template, title=default_title))

    redirects_dict = redirects.load_redirects(redirects_path)
    for partial_route in redirects_dict.keys():
        route = os.path.join('/redirect/', partial_route)
        if DEBUG:
            print('Route %s: Redirect %s' % (route, redirects_dict[partial_route]))
        app.add_url_rule(route, view_func=RedirectView.as_view(route_to_funcname(route), redirects_dict[partial_route]))

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    return app
