""" Licensed under the same terms as described in the main 
licensing script of this repository. """

from datetime import datetime
from pathlib import Path


def dump(
        path: Path, *, outname: Path,
        data: None
) -> None:
    """
    """
    now = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )
