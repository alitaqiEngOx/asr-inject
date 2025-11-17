""" Licensed under the same terms as described in the main 
licensing script of this repository. """

import argparse
import sys
from pathlib import Path

from asr_inject.operations import pipeline
from asr_inject.utils import log_handler, outtree


def main() -> int:
    """
    Pipeline entry point.
    """
    # parse input CLI arguments
    args = parse_args()

    # make outputs' directory
    outdir_name = outtree.make_global_outdir(
        Path(args.config).parent,
        return_name=True
    )

    # generate main logger object & log basic info
    logger = log_handler.generate(
        "ASR-inject",
        dir_name=(
            Path(args.config).parent / outdir_name
        )
    )

    logger.info("Welcome to ASR INJECT")
    logger.info(
        "Author: A. Taqi; "
        "alitaqi94.developer@gmail.com"
    )
    logger.info("All Rights Reserved\n  |")

    # run pipeline
    pipeline.run(
        Path(args.config), 
        outdir=Path(args.config).parent / outdir_name
    )

    # exit pipeline
    log_handler.exit_pipeline(
        logger, success=True
    )

    return 0

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
