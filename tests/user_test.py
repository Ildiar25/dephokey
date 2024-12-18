import unittest

from features.models.user import User

from shared.logger_setup import test_logger as logger


class TestUser(unittest.TestCase):
    def setUp(self) -> None:
        logger.info("Preparing USER instances...")

        # Create new instances
        self.user_01 = User("admin01", "admin@admin.com", "admin1234")
        self.user_02 = User("admin02", "admin@admin.com", "admin1234")

        logger.info("USER instances ready for test...")

    def tearDown(self) -> None:
        logger.info("Finishing USER test...")

    def test_print_instance(self) -> None:
        logger.debug(self.user_01)
        logger.debug(self.user_02)

    def test_user_fields(self) -> None:
        logger.info(">>> Starting USER fields test...")
        self.assertEqual(self.user_01.fullname, "admin01", "Should be 'admin01'...")
        self.assertEqual(self.user_01.email, "admin@admin.com", "Should be 'admin@admin.com'...")
        self.assertEqual(self.user_02.fullname, "admin02", "Should be 'admin02'...")
        self.assertEqual(self.user_02.email, "admin@admin.com", "Should be 'admin@admin.com'...")
