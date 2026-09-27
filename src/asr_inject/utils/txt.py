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

    lines = [
        "============= ASR-INJECT =============\n\n",
        (
            "* Author: A. Taqi; "
            "alitaqi94.developer@gmail.com\n"
        ),
        "* All Rights Reserved\n\n\n",
        f"### Outputs for: `{path.name}` ###\n",
        f"### Date/time generated: {now} ###\n\n\n",
    ]
