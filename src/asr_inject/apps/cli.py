""" Licensed under the same terms as described in the main 
licensing script of this repository. """

import argparse
import sys
from pathlib import Path

def main() -> int:
    """
    Pipeline entry point.
    """
    # parse input CLI arguments
    args = parse_args()

def parse_args() -> argparse.Namespace:
    """
    """
    parser = argparse.ArgumentParser(
        description=(
            "Compute aquifier-storage-and-recovery "
            "(ASR) efficiencies"
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--config",
        type=str,
        default=str(
            Path(__file__).parents[3] /
            "config" / "default.yml"
        ),
        help="path to your `.yml` configuration file"
    )

    return parser.parse_args()


if __name__ == "__main__":
    sys.exit(main())