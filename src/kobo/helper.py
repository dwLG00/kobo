def read(path):
    with open(path) as f:
        return f.read()

def gen_paths(cwd):
    contents_path = cwd / 'content'
    templates_path = cwd / 'templates'
    static_path = cwd / 'static'
    redirects_path = cwd / 'redirects.txt'
    frozen_path = cwd / 'routes-freeze.json'
    return (contents_path, templates_path, static_path, redirects_path, frozen_path)

def smart_capitalize(sentence):
    blacklist = ['and', 'the', 'of', 'to', 'by', 'in', 'a', 'for', 'as', 'but', 'it']
    tokens = sentence.split(' ')
    capitalized_tokens = []
    for i, token in enumerate(tokens):
        if i == 0 or (token not in blacklist):
            capitalized_tokens.append(token.capitalize())
        else:
            capitalized_tokens.append(token)
    return ' '.join(capitalized_tokens)
