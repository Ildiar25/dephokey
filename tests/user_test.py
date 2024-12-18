import unittest

from features.models.user import User

from shared.logger_setup import test_logger as logger


class TestUser(unittest.TestCase):
    def test_create_instance(self) -> None:
        logger.info("Starting test user...")

        # Create new instances
        user_01 = User("admin01", "admin@admin.com", "admin1234")
        user_02 = User("admin02", "admin@admin.com", "admin1234")
        self.assertEqual(user_01.fullname, "admin01", "Should be admin01")
        self.assertEqual(user_01.email, "admin@admin.com", "Should be admin@admin.com")
        self.assertEqual(user_02.fullname, "admin02", "Should be admin02")
        self.assertEqual(user_02.email, "admin@admin.com", "Should be admin@admin.com")

        # Register instance
        logger.debug(user_01)
        logger.debug(user_02)

        # Finish test
        logger.info("Ending test user...")
