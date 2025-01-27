import unittest

from features.models.user import User
from features.models.site import Site

from shared.logger_setup import test_logger as logger


class TestSite(unittest.TestCase):
    def setUp(self) -> None:
        logger.info("Preparing SITE instances...")

        self.user_test = User("admin", "admin@admin.com", "admin1234")

        # Create new instances
        self.site_01 = Site("www.test.com",
                            "admin01", "admin1234", self.user_test, "Test01")
        self.site_02 = Site("www.test.com",
                            "admin02", "admin1234", self.user_test, "Test02")
        self.site_03 = Site("www.test.com",
                            "admin03", "admin1234", self.user_test)

        logger.info("SITE instances ready for test...")

    def tearDown(self) -> None:
        logger.info("Finishing SITE test...")

    def test_print_instance(self) -> None:
        logger.debug(self.site_01)
        logger.debug(self.site_02)
        logger.debug(self.site_03)

    def test_site_fields(self) -> None:
        logger.info(">>> Starting SITE fields test...")
        self.assertEqual(self.site_01.name, "Test01", "Should be 'Test01'.")
        self.assertEqual(self.site_01.address, "www.test.com", "Should be 'www.test.com'...")
        self.assertEqual(self.site_02.username, "admin02", "Should be 'admin02'...")
        self.assertEqual(self.site_02.user, self.user_test, "Should be 'user_test'...")
        self.assertEqual(self.site_03.name, None, "Should be 'None'...")
