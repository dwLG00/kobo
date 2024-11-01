from flask import Flask, render_template, url_for, redirect
from flask.views import View
from gunicorn.app.base import BaseApplication
from . import parser
from . import redirects
import os

DEBUG=False

class MarkdownView(View):
    '''MarkdownView View

    This class should only be instantiated through cls.add_view(), as an argument for app.add_url_rule().
    Arguments:
    html     -- string containing markdown parsed to html to be inserted in template
    template -- relative route to template file
    title    -- title to be used for route
    '''
    def __init__(self, html, template, title):
        self.html = html
        self.template = template
        self.title = title
    def dispatch_request(self):
        '''Renders the specified template with markdown inserted and with specified title'''
        return render_template(self.template, md_parsed=self.html, title=self.title)

class RedirectView(View):
    '''RedirectView View

    This class shoudl only be instantiated through cls.add_view(), as an argument for app.add_url_rule().
    Arguments:
    target -- url to redirect to
    '''
    def __init__(self, target):
        self.target_url = target
    def dispatch_request(self):
        return redirect(self.target_url)

def create_server(root_directory, **kwargs):
    '''Returns a flask app object with routes pointing to compiled markdown files

    Arguments:
    root_directory     -- path to root directory of project, containing template and static directories

    Keyword Arguments:
    default_title      -- default title given to pages without specified title (default 'my-site')
    write              -- if true, parser saves route tree to '<root>/routes-freeze.json' to be
        read from later (default False)
    load_from_frozen   -- if true, loads route tree from '<root>/routes-freeze.json' instead of
        compiling tree again (default False)
    custom_view_routes -- dictionary of custom <route, (view, *arguments)> (default {})
    custom_view_route_override -- if true, routes specified in custom_view_routes will override (default
        False)
    '''
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

    custom_view_routes = kwargs.get('custom_view_routes', {}) # Dictionary of routes and tuple of view and args
    custom_view_route_override = kwargs.get('custom_view_route_override', False)

    def route_to_funcname(route):
        return route.replace('/', '_').replace('-', '_')

    if load_from_frozen:
        tree = parser.parse_tree_load(load_from_frozen)
    else:
        if write:
            tree = parser.parse_tree(contents_folder, write=True)
        else:
            tree = parser.parse_tree(contents_folder) # Outputs a list of routes and their paired html

    routes_added = []
    for route, html, title, template in tree:
        if route in custom_view_routes.keys() and custom_view_route_override: continue
        if DEBUG:
            print('Route %s (%s): %s' % (route, title, template))
        if title:
            app.add_url_rule(route, view_func=MarkdownView.as_view(route_to_funcname(route), html, template, title=title))
        else:
            app.add_url_rule(route, view_func=MarkdownView.as_view(route_to_funcname(route), html, template, title=default_title))
        routes_added.append(route)

    redirects_dict = redirects.load_redirects(redirects_path)
    for partial_route in redirects_dict.keys():
        route = os.path.join('/redirect/', partial_route)
        if route in custom_view_routes.keys() and custom_view_route_override: continue
        if DEBUG:
            print('Route %s: Redirect %s' % (route, redirects_dict[partial_route]))
        app.add_url_rule(route, view_func=RedirectView.as_view(route_to_funcname(route), redirects_dict[partial_route]))
        routes_added.append(route)

    for route in custom_view_routes.keys():
        view, *arguments = custom_view_routes[route]
        if not custom_view_route_override and route in routes_added:
            continue
        app.add_url_rule(route, view_func=view.as_view(*arguments))

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    return app

# Gunicorn stuff

class StandaloneApplication(BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
            if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application

def gunicornize(app, **options):
    return StandaloneApplication(app, options)
