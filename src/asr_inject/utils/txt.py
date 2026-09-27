""" Licensed under the same terms as described in the main 
licensing script of this repository. """

from datetime import datetime
from pathlib import Path
from typing import Any


def dump(
        path: Path, *, outname: Path,
        data: dict[str, Any]
) -> None:
    """
    """
    now = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    key_width = max(
        len(key) for key, _ in data
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
        f"{'PARAMETER':<{key_width}}   VALUE\n\n"
    ]

    for key, value in data.items():
        pass
