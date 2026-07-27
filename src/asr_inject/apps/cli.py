""" Licensed under the same terms as described in the main 
licensing script of this repository. """

import argparse
import sys
import time
from pathlib import Path

from asr_inject.operations import pipeline
from asr_inject.utils import log_handler, outtree


def main() -> int:
    """
    Pipeline entry point.
    """
    # start timer
    start_time = time.time()

    # generate main logger object
    main_logger = log_handler.enter_pipeline()

    try:
        # ----------------------------------------
        # 1. PARSE CLI ARGUMENTS
        # ----------------------------------------
        try:
            args = parse_args()

        # parser raises `SystemExit(0)` for `--help`
        except SystemExit as exc:
            if exc.code == 0:
                log_handler.exit_pipeline(
                    start_time=start_time
                )

                return 0

            raise

        # ----------------------------------------
        # 2. PIPELINE
        # ----------------------------------------
        main_logger.info("Entering pipeline")

        # make outputs' directory
        main_logger.info(
            "Generating outputs' directory"
        )

        outdir = outtree.make_global_outdir(
            Path(args.config).parent, return_name=True
        )

        # run pipeline
        pipeline.run(
            Path(args.config), 
            outdir=Path(args.config).parent / outdir
        )

        # ----------------------------------------
        # 3. SUCCESSFUL EXIT
        # ----------------------------------------
        log_handler.exit_pipeline(
            start_time=start_time, logger=main_logger,
            success=True
        )

        return 0

    except (Exception, SystemExit) as exc:
        # ----------------------------------------
        # 4. ERROR HANDLING
        # ----------------------------------------
        log_handler.exit_pipeline(
            start_time=start_time, logger=main_logger,
            error=exc
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
