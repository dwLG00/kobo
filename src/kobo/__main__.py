import argparse
from pathlib import Path
import shutil
import os
from . import helper
from . import parser
from . import server

# Global vars

CWD = Path.cwd()
CONTENTS_PATH, TEMPLATES_PATH, STATIC_PATH, REDIRECTS_PATH, FROZEN_PATH = helper.gen_paths(CWD)
#TODO FIGURE OUT HOW TO ADD THIS PART TO AN ACTUAL PACKAGE
INTERNAL_TEMPLATES_PATH = Path(__file__).parent / 'resources' / 'templates'
INTERNAL_STATIC_PATH = Path(__file__).parent / 'resources' / 'templates'

# Parser setup

parser = argparse.ArgumentParser(
    prog='kobo'
)
parser.add_argument('command', choices=['new', 'server', 'compile'])
parser.add_argument('-c', '--compile', action='store_true')
parser.add_argument('-g', '--gunicorn', action='store_true')
parser.add_argument('-p', '--port', type=int)
parser.add_argument('-L', '--load', action='store_true')
parser.add_argument('--title', type=str)


# Actually parse the args
args = parser.parse_args()
if args.command == 'new':
    CONTENTS_PATH.mkdir(parents=True, exist_ok=True)
    shutil.copytree(INTERNAL_TEMPLATES_PATH, TEMPLATES_PATH)
    shutil.copytree(INTERNAL_STATIC_PATH, STATIC_PATH)
    REDIRECTS_PATH.touch(exist_ok=True)
    print('Created new kobo project in %s' % str(CWD))
    exit(0)

if args.command == 'server':
    kwargs = {'write': args.compile, 'load_from_frozen': args.load, 'title': args.default_title}
    server_app = server.create_server(CWD, **kwargs)
    if not args.gunicorn:
        port = args.port if args.port else 8000
        app.run('0.0.0.0', port=port)
    else:
        pass #TODO Implement running gunicorn

if args.command == 'compile':
    parser.write_tree_save(CONTENTS_PATH, FROZEN_PATH)
    print('Saved routes to `%s`' % str(FROZEN_PATH))
    exit(0)
