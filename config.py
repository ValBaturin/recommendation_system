import os
import types

ROOT_PATH = '.'
HTML_PATH = ROOT_PATH + "/html/"
ARTICLE_PATH = ROOT_PATH + "/article/"

if __name__ == "__main__":
    for name, value in globals().copy().items():
        if not name.startswith('__') and type(value) is not types.ModuleType:
            print('{name} = {value}'.format(name=name, value=value))
