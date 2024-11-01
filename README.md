# Kobo
A hugo-like markdown website/blog builder + server

# Features
- Built with Flask
- Native support for markdown using katex
- Lots of out-of-the-box functionality
- Extensive customization options and extendibility

# Installation
1. Run `python3 -m pip install kobo-md`
2. Install katex via `npm install katex`

See [dylwall.com](http://dylwall.com) for a sample site built using kobo :)

# Usage
- To start a new project, simply enter the target directory and run `python3 -m kobo new`.
- To compile markdown files into html snippets, run `python3 -m kobo compile`.
- To run the server, run `python3 -m kobo server` from the project directory.

## Adding Content
- To create a page on your site, just make a markdown file in the `content` directory.
- By default, the route to your page will be the relative path to your file from the content directory.
    - Exception: If your filename is `index.md`, the route of the page will be the parent directory of the file. For example, `content/my-directory/index.md` will be routed to `/my-directory`.
    - If an `index.md` file is not present in a directory, an index page (but not file) for the directory will automatically be generated.
- By default, the title of your page will be the filename.

### Markdown Options
- You can override the default route and title of your page by setting them in your markdown file's header.
- You can also choose what template you want to use for your page in the header (see "Templates" for more info).
- You can choose to not publish a file by setting the `draft` option.
Here's an example markdown file with these options set:

```
---
title: My Page
route: /my-page
draft: false
template: homepage.html
---

# Welcome to My Page!
```

### Templates
- When pages in kobo are processed, they are inserted into [Jinja](https://jinja.palletsprojects.com/) files with a specific format.
- Index files use the `index.html` template and all other files use the `page.html` template by default. You can specify which template to use for a page in the markdown header.
- Template files are stored in the `templates` directory.

## Running
- To start up a server, just run `python3 -m kobo server`!
- Run `python3 -m kobo -h`

### Custom Configuration and Gunicorn
You can run the kobo flask app in your own scripts by importing `kobo.server.create_server`:

```
from kobo.server import create_server
from pathlib import Path

kwargs = {
    # Add your desired keyword arguments here
    'load_from_frozen': True,
    'default_title': "Dylan's Blog"
}

app = create_server(Path('/my/blog/root/directory'), **kwargs)

app.run('0.0.0.0', port=8080)
```

Alternatively, you can run kobo using gunicorn instead. All you have to do is omit the last line, and run `gunicorn -w 2 --bind 0.0.0.0:8000 'main:app'`.
