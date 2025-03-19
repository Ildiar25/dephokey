import unittest

from shared.logger_setup import logging, main_log, test_log


class TestLog(unittest.TestCase):
    def setUp(self) -> None:

        # Preparing both loggers
        self.test_log = test_log
        self.main_log = main_log

        # Main info message
        self.test_log.info(f"Logger inicializado en nivel: {logging.getLevelName(self.test_log.get_current_level())}")
        self.main_log.info(f"Logger inicializado en nivel: {logging.getLevelName(self.main_log.get_current_level())}")

    def test_all_levels(self) -> None:
        # Test log file (LEVEL DEBUG)
        self.test_log.debug("Esto es un mensaje en modo DEBUG")
        self.test_log.info("Esto es un mensaje en modo INFO")
        self.test_log.warning("Esto es un mensaje en modo WARNING")
        self.test_log.error("Esto es un mensaje en modo ERROR")
        self.test_log.critical("Esto es un mensaje en modo CRITICAL")

        # Main app log file (LEVEL WARNING)
        self.main_log.debug("Esto es un mensaje en modo DEBUG")
        self.main_log.info("Esto es un mensaje en modo INFO")
        self.main_log.warning("Esto es un mensaje en modo WARNING")
        self.main_log.error("Esto es un mensaje en modo ERROR")
        self.main_log.critical("Esto es un mensaje en modo CRITICAL")
