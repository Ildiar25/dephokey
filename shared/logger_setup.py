from logging.handlers import RotatingFileHandler
from pathlib import Path
import logging
import os


# Set logger settings
BASE_DIR = Path(__file__).parent.parent.joinpath("tests/logs")
LOG_LEVEL = os.getenv("LOG_LEVEL", "WARNING").strip().upper()


class Logger:
    """
    This class helps to create two loggers: One for file management and other for console. Both have the same level.

    Levels:
        DEBUG: Detailed information, typically only of interest to a developer trying to diagnose a problem.
        INFO: Confirmation that things are working as expected.
        WARNING: An indication about a problem might occur in the near future (e.g. ‘disk space low’).
        ERROR: Due to a more serious problem, the software has not been able to perform some function.
        CRITICAL: A serious error, indicating that the program itself may be unable to continue running.

    Documentation:
        https://docs.python.org/3/library/logging.html
    """
    def __init__(self, filename: str, level: str = "DEBUG") -> None:
        self.logger = logging.getLogger(BASE_DIR.joinpath(filename).__str__())
        self.logger.setLevel(self.__get_level(level))

        # Create a rotating file handler
        handler = RotatingFileHandler(
            filename=BASE_DIR.joinpath(filename).__str__(), maxBytes=1_000_000, backupCount=1, encoding="utf-8"
        )
        handler.setLevel(self.__get_level(level))

        # Create a console handler
        console = logging.StreamHandler()
        console.setLevel(self.__get_level(level))

        # Set formats
        file_date_format = "%Y-%m-%dT%H:%M:%S%z"
        file_log_format = "[%(asctime)s] ::: %(levelname)8s at line %(lineno)d from <%(module)s>: %(message)s"
        file_formatter = logging.Formatter(fmt=file_log_format, datefmt=file_date_format)
        console_date_format = "%H:%M:%S"
        console_log_format = "[%(asctime)s] | %(levelname)8s | Module: [%(name)s] | %(message)s"
        console_formatter = logging.Formatter(fmt=console_log_format, datefmt=console_date_format)

        handler.setFormatter(file_formatter)
        console.setFormatter(console_formatter)

        # Add handlers to logger
        self.logger.addHandler(handler)
        self.logger.addHandler(console)

    def get_current_level(self) -> int:
        return self.logger.getEffectiveLevel()

    def debug(self, msg: str) -> None:
        self.logger.debug(msg)

    def info(self, msg: str) -> None:
        self.logger.info(msg)

    def warning(self, msg: str) -> None:
        self.logger.warning(msg)

    def error(self, msg: str) -> None:
        self.logger.error(msg)

    def critical(self, msg: str) -> None:
        self.logger.critical(msg)

    @staticmethod
    def __get_level(level: str) -> int:
        levels = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL
        }
        return levels[level]


# Create file directory
if not BASE_DIR.is_dir():
    BASE_DIR.mkdir()

# Prepare loggers
main_log = Logger(filename="app.log", level=LOG_LEVEL)
test_log = Logger(filename="test_results.log")
