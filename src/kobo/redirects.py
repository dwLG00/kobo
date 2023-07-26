import os
import pathlib

def load_redirects(redirects_path) -> dict:
    with open(redirects_path) as f:
        lines = f.readlines()

    d = {}
    for line in lines:
        tokens = line.split(' ')
        assert len(tokens) == 2
        route = tokens[0].strip()
        target = tokens[1].strip()
        d[route] = target
    return d
