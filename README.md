# Kobo
A hugo-like markdown website/blog builder + server

# Features
- Built with Flask
- Native support for markdown using katex
- No customization -> forced to use the best web theme you've ever seen

# Installation
1. Clone the repo, then run `cd kobo` and `python3 setup.py install`
2. Install katex using `npm` by running `npm install katex`

# Usage
- To start a new project, simply enter the target directory and run `python3 -m katex new`.
- To run the server, run `python3 -m katex server` from the project directory.
- To compile markdown files into html snippets, run `python3 -m katex compile`.
