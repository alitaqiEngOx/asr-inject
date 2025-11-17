""" Licensed under the same terms as described in the main 
licensing script of this repository. """

import logging
import sys
from pathlib import Path


def exit_pipeline(
        logger: logging.Logger, *, success: bool=False
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
    logger.info("Exiting pipeline")

    if success:
        logger.info("Pipeline run - ✅ SUCCESS")

    else:
        logger.info("Pipeline run - ❌ FAILURE")
        sys.exit()

def generate(
        name: str, *, dir_name: Path
) -> logging.Logger:
    """
    Generates a new `logging.Logger` class instance.

    Arguments
    ---------
    name: `str`
        name given to the new class instance.

    dir_name: `pathlib.Path`
        directory into which the logfile is to be 
        saved.

    Returns
    -------
    New `logging.logger` class instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    dir_name.mkdir(
        parents=True, exist_ok=True
    )

    file_handler = logging.FileHandler(
        str(dir_name / "logfile.log")
    )

    file_handler.setFormatter(
        logging.Formatter(
                " +| %(name)s [%(asctime)s - "
                "%(levelname)s]: %(message)s"
            )
    )

    logger.addHandler(file_handler)

    return logger
