""" Licensed under the same terms as described in the main 
licensing script of this repository. """

from datetime import datetime
from pathlib import Path
from typing import Any

from asr_inject.utils.log_handler import create


LOGGER = create("txt")


def dump(
        data: dict[str, Any], *,
        outname: Path
) -> None:
    """
    """
    LOGGER.info(f"generating `{outname.name}`")

    now = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    key_lengths = [len(key) for key in data.keys()]
    key_lengths.append(len("PARAMETER"))

    max_key_length = max(key_lengths)

    lines = [
        "============= ASR-INJECT =============\n\n",
        (
            "* Author: A. Taqi; "
            "alitaqi94.developer@gmail.com\n"
        ),
        "* All Rights Reserved\n\n\n",
        f"### File name: `{outname.name}` ###\n",
        f"### Date/time generated: {now} ###\n\n\n",
        f"{'PARAMETER':<{max_key_length}}   VALUE\n\n"
    ]

    for key, value in data.items():
        lines.append(
            f"{key:<{max_key_length}} : {value}\n\n"
        )

    lines.append(
        "──────────── END ────────────\n\n\n"
    )

    lines.append(
        "============= ASR-INJECT ============="
    )

    with open(f"{outname}", 'w') as file:
        file.writelines(lines)
