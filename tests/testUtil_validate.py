import unittest

from shared.validate import Validate
from shared.logger_setup import test_logger as logger


class StringBuilder:
    def __init__(self) -> None:
        """Helps to create diferent elements."""
        self.__email = "testing.24@example.com"
        self.__password = "Testing_1234"
        self.__address = "http://www.testing-url.com"
        self.__number = "4033473536674460"
        self.__date = "01/91"

    def build(self, str_type: str) -> str:
        match str_type:
            case "email":
                element = self.__email
            case "password":
                element = self.__password
            case "address":
                element = self.__address
            case "number":
                element = self.__number
            case "date":
                element = self.__date
            case _:
                element = "unknown"
        return element


class TestValidate(unittest.TestCase):
    def setUp(self) -> None:
        logger.info("Preparing VALIDATE instance...")

        # Create comparable elements
        self.bad_email = ".testing@example.com"
        self.bad_password = "testing1234"
        self.bad_address = "http://testing_url.com"
        self.bad_number = "1234767634239989"
        self.bad_date = "03-25-1998"

        # Create new instance
        self.validate = Validate()

        logger.info("VALIDATE instance ready for test...")

    def tearDown(self) -> None:
        del self.validate

    def test_validateExists(self) -> None:
        self.log_instance(self.validate)
        self.assertIsNotNone(self.validate, msg="VALIDATE instance doesn't exist.")
        logger.info(">>> Confirm if VALIDATE exists...   OK")

    def test_validateType(self) -> None:
        self.assertIsInstance(self.validate, Validate, msg="Validate MUST BE validate type.")
        logger.info(">>> Confirm if VALIDATE is instance of VALIDATE...   OK")

    def test_validateEmailExists(self) -> None:
        self.log_string(StringBuilder().build("email"))
        self.assertIsNotNone(StringBuilder().build("email"), msg="EMAIL doesn't exist.")
        logger.info(">>> Confirm if EMAIL exists...   OK")

    def test_validateEmailType(self) -> None:
        self.assertIsInstance(StringBuilder().build("email"), str, msg="Email MUST BE string type.")
        logger.info(">>> Confirm if EMAIL is instance of STRING...   OK")

    def test_validateValidEmal(self) -> None:
        self.assertTrue(self.validate.is_valid_email(StringBuilder().build("email")),
                        msg="Email MUST BE a valid email.")
        logger.info(">>> Confirm if EMAIL is VALID...   OK")

    def test_validateNotValidEmail(self) -> None:
        self.log_string(self.bad_email)
        self.assertFalse(self.validate.is_valid_email(self.bad_email), msg="Bad email MUST BE an invalid emal.")
        logger.info(">>> Confirm if BAD EMAIL is INVALID...   OK")

    def test_validatePasswordExists(self) -> None:
        self.log_string(StringBuilder().build("password"))
        self.assertIsNotNone(StringBuilder().build("password"), msg="PASSWORD doesn't exist.")
        logger.info(">>> Confirm if PASSWORD exists...   OK")

    def test_validatePasswordType(self) -> None:
        self.assertIsInstance(StringBuilder().build("password"), str, msg="Password MUST BE string type.")
        logger.info(">>> Confirm if PASSWORD is instance of STRING...   OK")

    def test_validateValidPassword(self) -> None:
        self.assertTrue(self.validate.is_valid_password(StringBuilder().build("password")),
                        msg="Password MUST BE a valid password.")
        logger.info(">>> Confirm if PASSWORD is VALID...   OK")

    def test_validateInvalidPassword(self) -> None:
        self.log_string(self.bad_password)
        self.assertFalse(self.validate.is_valid_password(self.bad_password),
                         msg="Bad password MUST BE an invalid password.")
        logger.info(">>> Confirm if BAD PASSWORD is INVALID...   OK")

    def test_validateAddressExists(self) -> None:
        self.log_string(StringBuilder().build("address"))
        self.assertIsNotNone(StringBuilder().build("address"), msg="ADDRESS doesn't exist.")
        logger.info(">>> Confirm if ADDRESS exists...   OK")

    def test_validateAddressType(self) -> None:
        self.assertIsInstance(StringBuilder().build("address"), str, msg="Address MUST BE string type.")
        logger.info(">>> Confirm if ADDRESS is instance of STRING...   OK")

    def test_validateValidAddress(self) -> None:
        self.assertTrue(self.validate.is_valid_address(StringBuilder().build("address")),
                        msg="Address MUST BE a valid address.")
        logger.info(">>> Confirm if ADDRESS is VALID...   OK")

    def test_validateInvalidAddress(self) -> None:
        self.log_string(self.bad_address)
        self.assertFalse(self.validate.is_valid_address(self.bad_address),
                         msg="Bad address MUST BE an invalid address.")
        logger.info(">>> Confirm if BAD ADDRESS is INVALID...   OK")

    def test_validateNumberExists(self) -> None:
        self.log_string(StringBuilder().build("number"))
        self.assertIsNotNone(StringBuilder().build("number"), msg="CREDITCARD NUMBER doesn't exist.")
        logger.info(">>> Confirm if CREDITCARD NUMBER exists...   OK")

    def test_validateNumberType(self) -> None:
        self.assertIsInstance(StringBuilder().build("number"), str, msg="Creditcard number MUST BE string type.")
        logger.info(">>> Confirm if CREDITCARD NUMBER is instance of STRING...   OK")

    def test_validateValidNumber(self) -> None:
        self.assertTrue(self.validate.is_valid_creditcard_number(StringBuilder().build("number")),
                        msg="Creditcard number MUST BE a valid creditcard number.")
        logger.info(">>> Confirm if CREDITCARD NUMBER is VALID...   OK")

    def test_validateInvalidNumber(self) -> None:
        self.log_string(self.bad_number)
        self.assertFalse(self.validate.is_valid_creditcard_number(self.bad_number),
                         msg="Bad creditcard number MUST BE an invalid creditcard number.")
        logger.info(">>> Confirm if BAD CREDITCARD NUMBER is INVALID...   OK")

    def test_validateDateExists(self) -> None:
        self.log_string(StringBuilder().build("date"))
        self.assertIsNotNone(StringBuilder().build("date"), msg="DATE doesn't exist.")
        logger.info(">>> Confirm if DATE exists...   OK")

    def test_validateDateType(self) -> None:
        self.assertIsInstance(StringBuilder().build("date"), str, msg="Date MUST BE string type.")
        logger.info(">>> Confirm if DATE is instance of STRING...   OK")

    def test_validateValidDate(self) -> None:
        self.assertTrue(self.validate.is_valid_date(StringBuilder().build("date")),
                        msg="Date MUST BE a valid format date (mm-yy).")
        logger.info(">>> Confirm if DATE is VALID...   OK")

    def test_validateInvalidDate(self) -> None:
        self.log_string(self.bad_date)
        self.assertFalse(self.validate.is_valid_date(self.bad_date),
                         msg="Bad date MUST BE an invalid date.")
        logger.info(">>> Confirm if BAD DATE is INVALID...   OK")

    @staticmethod
    def log_instance(validator: Validate) -> None:
        logger.debug(validator)

    @staticmethod
    def log_string(text: str) -> None:
        logger.debug(text)


if __name__ == "__main__":
    unittest.main()
