"""
Strings manager
"""

import os
import json


_basedir = os.path.abspath(os.path.dirname(__file__))

# Load strings from json
_strings = json.loads(open(os.path.join(_basedir, 'strings.json'), 'r', encoding='utf8').read())


def get_string(key: str):
    return _strings.get(key, 'no_string')
