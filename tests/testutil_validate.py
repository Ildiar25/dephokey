import unittest

from shared.validate import Validate
from shared.logger_setup import test_logger as logger


class TestValidate(unittest.TestCase):
    def setUp(self) -> None:
        logger.info("Preparing VALIDATE instances...")

        self.valid_email = "example_22@example.com"
        self.invalid_email = "eXamPle_22.com"
        self.valid_password = "jknXhc78unweMjmjis5"
        self.invalid_password = "admin1234"
        self.valid_address = "http://www.example.com/"
        self.invalid_address = "example_com"
        self.valid_creditcard_number = "4111111111111111"
        self.invalid_creditcard_number = "4852154762351248"
        self.creditcard_not_number = "test01test01test"
        self.valid_date = ""
        self.invalid_date = ""

        # Create new instance
        self.validate = Validate()

        logger.info("VALIDATE instance ready for test...")

    def tearDown(self) -> None:
        logger.info("Finishing VALIDATE test...")

    def test_valid_email(self) -> None:
        logger.info(">>> Starting VALIDATE EMAIL test...")
        self.assertTrue(self.validate.is_valid_email(self.valid_email), "Should be 'example_22@example.com'...")
        self.assertFalse(self.validate.is_valid_email(self.invalid_email), "Should be 'eXamPle_22.com'...")

    def test_valid_password(self) -> None:
        logger.info(">>> Starting VALIDATE PASSWORD test...")
        self.assertTrue(self.validate.is_valid_password(self.valid_password),
                        "Should be 'http://www.example.com/'...")
        self.assertFalse(self.validate.is_valid_password(self.invalid_password),
                         "Should be 'admin1234'...")

    def test_valid_address(self) -> None:
        logger.info(">>> Starting VALIDATE ADDRESS test...")
        self.assertTrue(self.validate.is_valid_address(self.valid_address),
                        "Should be 'jknXhc78unweMjmjis5'...")
        self.assertFalse(self.validate.is_valid_address(self.invalid_address),
                         "Should be 'example.com'...")

    def test_valid_creditcard_number(self) -> None:
        logger.info(">>> Starting VALIDATE CREDITCARD NUMBER test...")
        self.assertTrue(self.validate.is_valid_creditcard_number(self.valid_creditcard_number),
                        "Should be '4111111111111111'...")
        self.assertFalse(self.validate.is_valid_creditcard_number(self.invalid_creditcard_number),
                         "Should be '4852154762351248'...")
        self.assertFalse(self.validate.is_valid_creditcard_number(self.creditcard_not_number),
                         "Should be 'test01test01test'...")
