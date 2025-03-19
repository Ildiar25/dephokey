import unittest

from shared.logger_setup import logging, main_log, test_log


class TestLog(unittest.TestCase):
    def setUp(self) -> None:

        # Preparing both loggers
        self.test_log = test_log
        self.main_log = main_log

        # Prepare levels
        self.test_level = 10  # DEBUG LEVEL
        self.main_level = 30  # WARNING LEVEL

        # Main info message
        self.test_log.info(f"Logger initialized in level: {logging.getLevelName(self.test_log.get_current_level())}")
        self.main_log.info(f"Logger initialized in level: {logging.getLevelName(self.main_log.get_current_level())}")

    def test_all_levels(self) -> None:
        # Test log file (LEVEL DEBUG)
        self.test_log.debug("This is a DEBUG LEVEL example message")
        self.test_log.info("This is a INFO LEVEL example message")
        self.test_log.warning("This is a WARNING LEVEL example message")
        self.test_log.error("This is a ERROR LEVEL example message")
        self.test_log.critical("This is a CRITICAL LEVEL example message")

        # Main app log file (LEVEL WARNING)
        self.main_log.debug("This is a DEBUG LEVEL example message")
        self.main_log.info("This is a INFO LEVEL example message")
        self.main_log.warning("This is a WARNING LEVEL example message")
        self.main_log.error("This is a ERROR LEVEL example message")
        self.main_log.critical("This is a CRITICAL LEVEL example message")

    def test_testLevel(self) -> None:
        self.assertEqual(
           first=self.test_level,
           second=self.test_log.get_current_level(),
           msg="Actually TEST LOG LEVEL is not setted as DEBUG"
        )
        self.test_log.info(">>> Confirm test log level is DEBUG...   OK")

    def test_mainLevel(self) -> None:
        self.assertEqual(
            first=self.main_level,
            second=self.main_log.get_current_level(),
            msg="Actually MAIN LOG LEVEL is not setted as WARNING"
        )
        self.test_log.info(">>> Confirm main log level is WARNING...   OK")


if __name__ == "__main__":
    unittest.main()
