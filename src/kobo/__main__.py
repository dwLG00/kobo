import argparse
from pathlib import Path
import shutil
import os
import multiprocessing
from . import helper
from . import parser
from . import server

# Global vars

CWD = Path.cwd()
CONTENT_PATH, TEMPLATES_PATH, STATIC_PATH, REDIRECTS_PATH, FROZEN_PATH = helper.gen_paths(CWD)
INTERNAL_TEMPLATES_PATH = Path(__file__).parent / 'resources' / 'templates'
INTERNAL_STATIC_PATH = Path(__file__).parent / 'resources' / 'static'
INTERNAL_CONTENT_PATH = Path(__file__).parent / 'resources' / 'content'

# Parser setup

argparser = argparse.ArgumentParser(
    prog='kobo'
)
argparser.add_argument('command', choices=['new', 'server', 'compile'])
argparser.add_argument('-c', '--compile', action='store_true')
argparser.add_argument('-g', '--gunicorn', action='store_true')
argparser.add_argument('-p', '--port', type=int)
argparser.add_argument('-L', '--load', action='store_true')
argparser.add_argument('--title', type=str)


# Actually parse the args
args = argparser.parse_args()
if args.command == 'new':
    shutil.copytree(INTERNAL_CONTENT_PATH, CONTENT_PATH)
    shutil.copytree(INTERNAL_TEMPLATES_PATH, TEMPLATES_PATH)
    shutil.copytree(INTERNAL_STATIC_PATH, STATIC_PATH)
    REDIRECTS_PATH.touch(exist_ok=True)
    print('Created new kobo project in %s' % str(CWD))
    exit(0)

if args.command == 'server':
    kwargs = {'write': args.compile, 'load_from_frozen': args.load, 'default_title': args.title}
    server_app = server.create_server(CWD, **kwargs)
    port = args.port if args.port else 8000
    if not args.gunicorn:
        server_app.run('0.0.0.0', port=port)
    else:
        options = {
            'bind': '0.0.0.0:%s' % port,
            'workers': min(((multiprocessing.cpu_count() * 2) + 1), 4),
            'timeout': 120
        }
        gunicorn_app = server.gunicornize(server_app, **options)
        gunicorn_app.run()

    exit(0)

if args.command == 'compile':
    parser.parse_tree_save(CONTENT_PATH, FROZEN_PATH)
    print('Saved routes to `%s`' % str(FROZEN_PATH))
    exit(0)
