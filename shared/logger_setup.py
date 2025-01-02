import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

"""
# ----- LEVELS ----- #

· DEBUG: Detailed information, typically only of interest to a developer trying to diagnose a problem.
· INFO: Confirmation that things are working as expected.
· WARNING: An indication about a problem might occur in the near future (e.g. ‘disk space low’).
· ERROR: Due to a more serious problem, the software has not been able to perform some function.
· CRITICAL: A serious error, indicating that the program itself may be unable to continue running.

# ----- DOCUMENTATION ----- #

https://docs.python.org/3/library/logging.html
"""


# Creates generic function
def setup_logger(name: str, path: Path, mode: str, file_size: int, text_format: logging.Formatter,
                 level: int = logging.DEBUG) -> logging.Logger:

    # Sets file handler
    file_handler = RotatingFileHandler(
        filename=path,
        mode=mode,
        maxBytes=file_size,
        backupCount=1,
        encoding="utf-8",
    )
    file_handler.setFormatter(text_format)

    # Sets log data
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(file_handler)

    # Return logger
    return logger


# Set base directory
BASE_DIR = Path(__file__).parent.parent

# Create file directory
if not BASE_DIR.joinpath("tests/logs/").is_dir():
    BASE_DIR.joinpath("tests/logs/").mkdir()

# Sets the files name
FILE_TEST_NAME = "test_logs.log"
MAIN_FILE_NAME = "app_logs.log"

# Generic text-format setup
date_format = "%Y-%m-%dT%H:%M:%S%z"
log_format = logging.Formatter(
    fmt="[%(asctime)s]:::%(levelname)s at line %(lineno)d from <%(module)s>: %(message)s",
    datefmt=date_format
)

test_logger = setup_logger(
    name="test_logger",
    path=BASE_DIR.joinpath("tests/logs/" + FILE_TEST_NAME),
    mode="w",
    file_size=1048576,
    text_format=log_format
)

main_logger = setup_logger(
    name="main_logger",
    path=BASE_DIR.joinpath("tests/logs/" + MAIN_FILE_NAME),
    mode="a",
    file_size=3072,
    text_format=log_format,
    level=logging.WARNING
)
