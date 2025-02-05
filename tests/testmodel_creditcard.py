import unittest
import datetime

from features.models.user import User
from features.models.creditcard import CreditCard

from shared.logger_setup import test_logger as logger


class TestCreditCard(unittest.TestCase):
    def setUp(self) -> None:
        logger.info("Preparing CREDITCARD instances...")

        user_test = User("admin", "admin@admin.com", "admin1234")
        future_date = datetime.datetime(2026, 5, 1)
        expired_date = datetime.datetime(2020, 5, 1)

        # Create new instances
        self.creditcard_01 = CreditCard(
            "Admin01", "1234567891234567", "123", future_date, user_test
        )
        self.creditcard_02 = CreditCard(
            "Admin02", "1234567891234567", "123", expired_date, user_test, "test"
        )

        logger.info("CREDITCARD instances ready for test...")

    def tearDown(self) -> None:
        logger.info("Finishing CREDITCARD test...")

    def test_print_instance(self) -> None:
        logger.debug(self.creditcard_01)
        logger.debug(self.creditcard_02)

    def test_creditcard_fields(self) -> None:
        logger.info(">>> Starting CREDITCARD fields test...")
        self.assertEqual(self.creditcard_01.cardholder, "Admin01", "Should be 'Admin'...")
        self.assertEqual(self.creditcard_01.alias, None, "Should be 'None'...")
        self.assertEqual(self.creditcard_02.cardholder, "Admin02", "Should be 'Admin02'...")
        self.assertEqual(self.creditcard_02.alias, "test", "Should be 'test'...")

    def test_is_expired_test(self) -> None:
        logger.info(">>> Starting CREDITCARD expired test...")
        self.assertFalse(self.creditcard_01.expired)
        self.assertTrue(self.creditcard_02.expired)
