"""
Utils for testing
"""

import json
import os


DIRNAME = os.path.dirname(__file__)


def load_json_from_file(filename) -> str:
    """Loads json from a file"""
    fixtures_dir = DIRNAME + '/fixtures/'
    full_path = os.path.join(
        fixtures_dir,
        filename
    )
    with open(full_path, 'r', encoding='utf-8') as json_file:
        json_text = json.load(json_file)
        return json_text
