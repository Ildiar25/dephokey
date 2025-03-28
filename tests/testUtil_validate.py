import unittest

from shared.logger_setup import test_log as log
from shared.validate import Validate


class StringBuilder:
    def __init__(self) -> None:
        """Helps to create diferent elements."""
        self.__address = "http://www.testing-url.com"
        self.__date = "01/91"
        self.__email = "testing.24@example.com"
        self.__number = "4033473536674460"
        self.__password = "Testing_1234"

    def build(self, str_type: str) -> str:
        match str_type:
            case "address":
                item = self.__address
            case "date":
                item = self.__date
            case "email":
                item = self.__email
            case "number":
                item = self.__number
            case "password":
                item = self.__password
            case _:
                item = "unknown"

        return item


class TestValidate(unittest.TestCase):
    def setUp(self) -> None:
        log.info("Preparing VALIDATE instance...")

        # Create comparable elements
        self.bad_address = "http://testing_url.com"
        self.bad_date = "03-25-1998"
        self.bad_email = ".testing@example.com"
        self.bad_number = "1234767634239989"
        self.bad_password = "testing1234"

        # Create new instance
        self.validate = Validate()

        log.info("VALIDATE instance ready for test...")

    def tearDown(self) -> None:
        del self.validate

    def test_validateExists(self) -> None:
        self.log_instance(self.validate)
        self.assertIsNotNone(
            obj=self.validate,
            msg="VALIDATE instance doesn't exist."
        )
        log.info(">>> Confirm if VALIDATE exists...   OK")

    def test_validateType(self) -> None:
        self.assertIsInstance(
            obj=self.validate,
            cls=Validate,
            msg="Validate MUST BE validate type."
        )
        log.info(">>> Confirm if VALIDATE is instance of VALIDATE...   OK")

    def test_validateEmailExists(self) -> None:
        self.log_string(StringBuilder().build("email"))
        self.assertIsNotNone(
            obj=StringBuilder().build("email"),
            msg="EMAIL doesn't exist."
        )
        log.info(">>> Confirm if EMAIL exists...   OK")

    def test_validateEmailType(self) -> None:
        self.assertIsInstance(
            obj=StringBuilder().build("email"),
            cls=str,
            msg="Email MUST BE string type."
        )
        log.info(">>> Confirm if EMAIL is instance of STRING...   OK")

    def test_isValidEmail(self) -> None:
        self.assertTrue(
            expr=self.validate.is_valid_email(StringBuilder().build("email")),
            msg="Email MUST BE a valid email."
        )
        log.info(">>> Confirm if EMAIL is VALID...   OK")

    def test_isNotValidEmail(self) -> None:
        self.log_string(self.bad_email)
        self.assertFalse(
            expr=self.validate.is_valid_email(self.bad_email),
            msg="Bad email MUST BE an invalid emal."
        )
        log.info(">>> Confirm if BAD EMAIL is INVALID...   OK")

    def test_validatePasswordExists(self) -> None:
        self.log_string(StringBuilder().build("password"))
        self.assertIsNotNone(
            obj=StringBuilder().build("password"),
            msg="PASSWORD doesn't exist."
        )
        log.info(">>> Confirm if PASSWORD exists...   OK")

    def test_validatePasswordType(self) -> None:
        self.assertIsInstance(
            obj=StringBuilder().build("password"),
            cls=str,
            msg="Password MUST BE string type."
        )
        log.info(">>> Confirm if PASSWORD is instance of STRING...   OK")

    def test_isValidPassword(self) -> None:
        self.assertTrue(
            expr=self.validate.is_valid_password(StringBuilder().build("password")),
            msg="Password MUST BE a valid password."
        )
        log.info(">>> Confirm if PASSWORD is VALID...   OK")

    def test_isNotValidPassword(self) -> None:
        self.log_string(self.bad_password)
        self.assertFalse(
            expr=self.validate.is_valid_password(self.bad_password),
            msg="Bad password MUST BE an invalid password."
        )
        log.info(">>> Confirm if BAD PASSWORD is INVALID...   OK")

    def test_validateAddressExists(self) -> None:
        self.log_string(StringBuilder().build("address"))
        self.assertIsNotNone(
            obj=StringBuilder().build("address"),
            msg="ADDRESS doesn't exist."
        )
        log.info(">>> Confirm if ADDRESS exists...   OK")

    def test_validateAddressType(self) -> None:
        self.assertIsInstance(
            obj=StringBuilder().build("address"),
            cls=str,
            msg="Address MUST BE string type."
        )
        log.info(">>> Confirm if ADDRESS is instance of STRING...   OK")

    def test_isValidAddress(self) -> None:
        self.assertTrue(
            expr=self.validate.is_valid_address(StringBuilder().build("address")),
            msg="Address MUST BE a valid address."
        )
        log.info(">>> Confirm if ADDRESS is VALID...   OK")

    def test_isNotValidAddress(self) -> None:
        self.log_string(self.bad_address)
        self.assertFalse(
            expr=self.validate.is_valid_address(self.bad_address),
            msg="Bad address MUST BE an invalid address."
        )
        log.info(">>> Confirm if BAD ADDRESS is INVALID...   OK")

    def test_validateNumberExists(self) -> None:
        self.log_string(StringBuilder().build("number"))
        self.assertIsNotNone(
            obj=StringBuilder().build("number"),
            msg="CREDITCARD NUMBER doesn't exist."
        )
        log.info(">>> Confirm if CREDITCARD NUMBER exists...   OK")

    def test_validateNumberType(self) -> None:
        self.assertIsInstance(
            obj=StringBuilder().build("number"),
            cls=str,
            msg="Creditcard number MUST BE string type."
        )
        log.info(">>> Confirm if CREDITCARD NUMBER is instance of STRING...   OK")

    def test_isValidNumber(self) -> None:
        self.assertTrue(
            expr=self.validate.is_valid_creditcard_number(StringBuilder().build("number")),
            msg="Creditcard number MUST BE a valid creditcard number."
        )
        log.info(">>> Confirm if CREDITCARD NUMBER is VALID...   OK")

    def test_isNotValidNumber(self) -> None:
        self.log_string(self.bad_number)
        self.assertFalse(
            expr=self.validate.is_valid_creditcard_number(self.bad_number),
            msg="Bad creditcard number MUST BE an invalid creditcard number."
        )
        log.info(">>> Confirm if BAD CREDITCARD NUMBER is INVALID...   OK")

    def test_validateDateExists(self) -> None:
        self.log_string(StringBuilder().build("date"))
        self.assertIsNotNone(
            obj=StringBuilder().build("date"),
            msg="DATE doesn't exist."
        )
        log.info(">>> Confirm if DATE exists...   OK")

    def test_validateDateType(self) -> None:
        self.assertIsInstance(
            obj=StringBuilder().build("date"),
            cls=str,
            msg="Date MUST BE string type."
        )
        log.info(">>> Confirm if DATE is instance of STRING...   OK")

    def test_isValidDate(self) -> None:
        self.assertTrue(
            expr=self.validate.is_valid_date(StringBuilder().build("date")),
            msg="Date MUST BE a valid format date (mm-yy)."
        )
        log.info(">>> Confirm if DATE is VALID...   OK")

    def test_isNotValidDate(self) -> None:
        self.log_string(self.bad_date)
        self.assertFalse(
            expr=self.validate.is_valid_date(self.bad_date),
            msg="Bad date MUST BE an invalid date."
        )
        log.info(">>> Confirm if BAD DATE is INVALID...   OK")

    @staticmethod
    def log_instance(validator: Validate) -> None:
        log.debug(validator)

    @staticmethod
    def log_string(text: str) -> None:
        log.debug(text)


if __name__ == "__main__":
    unittest.main()
