""" Licensed under the same terms as described in the main 
licensing script of this repository. """

import yaml
from pathlib import Path
from typing import Any


def read_yaml(dir: Path) -> dict[str, Any]:
    """
    """
    with open(f"{dir}", 'r') as file:
        return yaml.safe_load(file)
