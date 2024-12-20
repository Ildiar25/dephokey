import logging
from logging.handlers import RotatingFileHandler
import os

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
def setup_logger(name: str, path: str, file_size: int, text_format: logging.Formatter,
                 level: int = logging.DEBUG) -> logging.Logger:

    # Sets file handler
    file_handler = RotatingFileHandler(
        filename=path,
        mode="a",
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


# Sets the files name
FILE_TEST_NAME = "logs/test_logs.log"
MAIN_LOG_NAME = "app_logs.log"

# Generic text-format setup
date_format = "%Y-%m-%dT%H:%M:%S%z"
log_format = logging.Formatter(
    fmt="[%(asctime)s]:::%(levelname)s at line %(lineno)d from <%(module)s>: %(message)s",
    datefmt=date_format
)

test_logger = setup_logger(
    "test_logger",
    FILE_TEST_NAME,
    3072,
    log_format
)

main_logger = setup_logger(
    "main_logger",
    MAIN_LOG_NAME,
    1048576,
    log_format,
    logging.WARNING
)

something = os.getenv("LOG_LEVEL")
print(something)
