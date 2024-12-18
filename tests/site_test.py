import unittest

from features.models.user import User
from features.models.site import Site

from shared.logger_setup import test_logger as logger


class TestSite(unittest.TestCase):
    def test_create_instance(self):
        logger.info("Starting Site test...")

        user_test = User("admin", "admin@admin.com", "admin1234")

        # Create new instances
        site_01 = Site("Test01", "www.test.com", "admin01", "admin1234", user_test)
        site_02 = Site("Test02", "www.test.com", "admin02", "admin1234", user_test)
        self.assertEqual(site_01.name, "Test01", "Should be 'Test01'.")
        self.assertEqual(site_01.address, "www.test.com", "Should be 'www.test.com'.")
        self.assertEqual(site_02.username, "admin02", "Should be 'admin02'.")
        self.assertEqual(site_02.user, user_test, "Should be 'user_test'.")

        # register instance
        logger.debug(site_01)
        logger.debug(site_02)

        # Finish test
        logger.info("Finishing Site test...")
