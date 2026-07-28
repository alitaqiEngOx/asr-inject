""" Licensed under the same terms as described in the main 
licensing script of this repository. """

import logging
import sys
import time
import traceback
from pathlib import Path


def create(
        name: str, *, header_footer: bool=False
) -> logging.Logger:
    """
    Generates a new `logging.Logger` class instance.

    Arguments
    ---------
    name: `str`
        name given to the new class instance.

    header_footer: `bool=False`
        if `True`, treats the logger as a 
        header/footer.

    Returns
    -------
    New `logging.logger` class instance.
    """
    while len(name) < 10:
        name += ' '

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if header_footer:
        formatter = logging.Formatter('')

    else:
        formatter = logging.Formatter(
            " +| %(name)s [%(asctime)s -"
            " %(levelname)s]: %(message)s"
        )

    stream_handler = logging.StreamHandler()

    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


def enter_pipeline() -> logging.Logger:
    """
    """
    header_logger = create(
        "header", header_footer=True
    )

    header_logger.info(
        "\n========== ASR-INJECT ==========\n"
    )

    header_logger.info(
        " * Author: A. Taqi;"
        " alitaqi94.developer@gmail.com\n"
    )
    header_logger.info(" * All Rights Reserved\n")

    return create("main")


def exit_pipeline(
        *, start_time: float,
        logger: logging.Logger | None=None,
        success: bool | None=None,
        error: BaseException | None=None
) -> None:
    """
    Exits the pipeline gracefully.

    Arguments
    ---------
    logger: `logging.Logger`
        logger object to exit the pipeline with.

    success: `bool=False`
        optional argument which, if `True`, the pipeline
        declares a successful run as it ends the job,
        but declares a failed run otherwise.
    """
    footer_logger = create(
        "footer", header_footer=True
    )

    # neutral exit (e.g., parser called with `--help` tag)
    if success is None and error is None:
        footer_logger.info(
            "\n========== ASR-INJECT ==========\n"
        )

        return

    logger = (
        footer_logger if logger is None
        else logger
    )

    # error repoted -> pipeline MUST fail
    if error is not None:
        logger.error("▼▼▼ Exception occurred ▼▼▼\n")

        exception_logger = create(
            "exception", header_footer=True
        )

        exception_logger.error(
            f"{type(error).__name__}: {error}\n"
        )

        exception_logger.error("────── TRACEBACK ──────\n")

        exception_logger.error(
            "".join(
                traceback.format_exception(
                    type(error),
                    error,
                    error.__traceback__,
                )
            )
        )

        exception_logger.error("──── END TRACEBACK ────\n")

        logger.info("Pipeline run - ❌ FAILURE")
        logger.info(f"Exiting pipeline")
        logger.info(
            f"Full time ="
            f" {round(time.time() - start_time, 3)} s"
        )

        footer_logger.info(
            "\n========== ASR-INJECT ==========\n"
        )

        if isinstance(error, SystemExit):
            exit_code = (
                error.code
                if isinstance(error.code, int)
                else 1
            )

            if exit_code == 0:
                exit_code = 1

            sys.exit(exit_code)

        sys.exit(1)

    # success/failure reported and no error given
    if success:
        logger.info(f"Pipeline run - ✅ SUCCESS")

    else:
        logger.info("Pipeline run - ❌ FAILURE")

    logger.info(f"Exiting pipeline")
    logger.info(
        f"Full time ="
        f" {round(time.time() - start_time, 3)} s"
    )

    footer_logger.info(
        "\n========== ASR-INJECT ==========\n"
    )

    if not success:
        sys.exit(1)
