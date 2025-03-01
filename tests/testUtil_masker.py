import unittest

from shared.logger_setup import test_log as log
from shared.utils.masker import *


class StringBuilder:
    def __init__(self) -> None:
        """Helps to create diferent elements."""
        self.__email = "testing.24@example.com"
        self.__username = "TestingName"
        self.__password = "Testing1234"
        self.__number = "1234767634239989"
        self.__phone = "666333454"
        self.__text = "This is a test. All examples used in this session are too basics."

    def build(self, str_type: str) -> str:
        match str_type:
            case "email":
                element = self.__email
            case "username":
                element = self.__username
            case "password":
                element = self.__password
            case "number":
                element = self.__number
            case "phone":
                element = self.__phone
            case "text":
                element = self.__text
            case _:
                element = "unknown"
        return element


class TestMasker(unittest.TestCase):
    def setUp(self) -> None:
        log.info("Preparing MASKER testing...")

        # Create comparable elements
        self.masked_email = "••••••••••@example.com"
        self.masked_username = "Tes••••••••"
        self.masked_password = "•••••••••••"
        self.masked_number = "••••••••••••9989"
        self.masked_phone = "••••••454"
        self.masked_text = "•••• •• • ••••• ••• •••••••• •••• •• •••• ••••••• ••• ••• •••••••"

        log.info("MASKER ready for test...")

    def test_maskerEmailExists(self) -> None:
        self.log_string(StringBuilder().build("email"))
        self.assertIsNotNone(StringBuilder().build("email"), msg="EMAIL doesn't exist.")
        log.info(">>> Confirm if EMAIL exists...   OK")

    def test_maskerEmailType(self) -> None:
        self.assertIsInstance(StringBuilder().build("email"), str, msg="Email MUST BE string type.")
        log.info(">>> Confirm if EMAIL is instance of STRING...   OK")

    def test_maskerEmailMasked(self) -> None:
        self.log_string(mask_email(StringBuilder().build("email")))
        self.assertEqual(self.masked_email, mask_email(StringBuilder().build("email")),
                         msg="Email content MUST BE equal.")
        log.info(">>> Confirm if EMAIL is MASKED...   OK")

    def test_maskerUsernameExists(self) -> None:
        self.log_string(StringBuilder().build("username"))
        self.assertIsNotNone(StringBuilder().build("username"), msg="USERNAME doesn't exist.")
        log.info(">>> Confirm if USERNAME exists...   OK")

    def test_maskerUsernameType(self) -> None:
        self.assertIsInstance(StringBuilder().build("username"), str, msg="Username MUST BE string type.")
        log.info(">>> Confirm if USERNAME is instance of STRING...   OK")

    def test_maskerUsernameMasked(self) -> None:
        self.log_string(mask_username(StringBuilder().build("username")))
        self.assertEqual(self.masked_username, mask_username(StringBuilder().build("username")),
                         msg="Username content MUST BE equal.")
        log.info(">>> Confirm if USERNAME is MASKED...   OK")

    def test_maskerPasswordExists(self) -> None:
        self.log_string(StringBuilder().build("password"))
        self.assertIsNotNone(StringBuilder().build("password"), msg="PASSWORD doesn't exist.")
        log.info(">>> Confirm if PASSWORD exists...   OK")

    def test_maskerPasswordType(self) -> None:
        self.assertIsInstance(StringBuilder().build("password"), str, msg="Password MUST BE string type.")
        log.info(">>> Confirm if PASSWORD is instance of STRING...   OK")

    def test_maskerPasswordMasked(self) -> None:
        self.log_string(mask_password(StringBuilder().build("password")))
        self.assertEqual(self.masked_password, mask_password(StringBuilder().build("password")),
                         msg="Password content MUST BE equal.")
        log.info(">>> Confirm if PASSWORD is MASKED...   OK")

    def test_maskerNumberExists(self) -> None:
        self.log_string(StringBuilder().build("number"))
        self.assertIsNotNone(StringBuilder().build("number"), msg="NUMBER doesn't exist.")
        log.info(">>> Confirm if NUMBER exists...   OK")

    def test_maskerNumberType(self) -> None:
        self.assertIsInstance(StringBuilder().build("number"), str, msg="Number MUST BE string type.")
        log.info(">>> Confirm if NUMBER is instance of STRING...   OK")

    def test_maskerNumberMasked(self) -> None:
        self.log_string(mask_number(StringBuilder().build("number")))
        self.assertEqual(self.masked_number, mask_number(StringBuilder().build("number")),
                         msg="Number content MUST BE equal.")
        log.info(">>> Confirm if NUMBER is MASKED...   OK")

    def test_maskerPhoneExists(self) -> None:
        self.log_string(StringBuilder().build("phone"))
        self.assertIsNotNone(StringBuilder().build("phone"), msg="PHONE doesn't exist.")
        log.info(">>> Confirm if PHONE exists...   OK")

    def test_maskerPhoneType(self) -> None:
        self.assertIsInstance(StringBuilder().build("phone"), str, msg="Phone MUST BE string type.")
        log.info(">>> Confirm if PHONE is instance of STRING...   OK")

    def test_maskerPhoneMasked(self) -> None:
        self.log_string(mask_phone(StringBuilder().build("phone")))
        self.assertEqual(self.masked_phone, mask_phone(StringBuilder().build("phone")),
                         msg="Phone content MUST BE equal.")
        log.info(">>> Confirm if PHONE is MASKED...   OK")

    def test_maskerTextExists(self) -> None:
        self.log_string(StringBuilder().build("text"))
        self.assertIsNotNone(StringBuilder().build("text"), msg="TEXT doesn't exist.")
        log.info(">>> Confirm if TEXT exists...   OK")

    def test_maskerTextType(self) -> None:
        self.assertIsInstance(StringBuilder().build("text"), str, msg="Text MUST BE string type.")
        log.info(">>> Confirm if TEXT is instance of STRING...   OK")

    def test_maskerTextMasked(self) -> None:
        self.log_string(mask_text(StringBuilder().build("text")))
        self.assertEqual(self.masked_text, mask_text(StringBuilder().build("text")),
                         msg="Text content MUST BE equal.")
        log.info(">>> Confirm if TEXT is MASKED...   OK")

    @staticmethod
    def log_string(text: str) -> None:
        log.debug(text)

if __name__ == "__main__":
    unittest.main()
