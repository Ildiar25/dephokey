import unittest
import datetime

from features.models.user import User
from features.models.password_request import PasswordRequest

from shared.logger_setup import test_logger as logger


class TestPasswordRequest(unittest.TestCase):
    def setUp(self) -> None:
        logger.info("Preparing PASSWORD REQUEST instances...")

        self.user_test = User("admin", "admin@admin.com", "admin1234")
        self.future_date = datetime.datetime.today() + datetime.timedelta(minutes=15)
        self.expired_date = datetime.datetime.today() - datetime.timedelta(minutes=15)

        # Create new instances
        self.request_01 = PasswordRequest(self.user_test)
        self.request_02 = PasswordRequest(self.user_test)

        logger.info("PASSWORD REQUEST instances ready for test...")

    def tearDown(self) -> None:
        logger.info("Finishing PASSWORD REQUEST test...")

    def test_print_instance(self) -> None:
        logger.debug(self.request_01)
        logger.debug(self.request_02)

    def test_password_request_field(self) -> None:
        logger.info(">>> Starting PASSWORD REQUEST field test...")
        self.assertEqual(self.request_01.user, self.user_test, "Should be 'user_test'...")
        self.assertEqual(self.request_02.user, self.user_test, "Should be 'user_test'...")

    def test_expired_request(self) -> None:
        logger.info(">>> Starting PASSWORD REQUEST expired request test...")
        self.assertGreater(self.request_01.created, self.expired_date, "Should be ''...")
        self.assertLess(self.request_02.created, self.future_date, "Should be ''...")
