import unittest
from types import NoneType
import datetime as dt

from features.data_encryption.core import decrypt_data
from features.models.user import User, UserRole
from features.models.creditcard import CreditCard

from shared.logger_setup import test_logger as logger


class UserBuilder:
    def __init__(self) -> None:
        """Helps to create a User instance."""
        self.__user = User(fullname="UserTest Name", email="user.email@example.com", password="User_1234")

    def with_role(self, new_role: UserRole) -> "UserBuilder":
        self.__user.role = new_role
        return self

    def build(self) -> User:
        return self.__user


class CreditCardBuilder:
    def __init__(self) -> None:
        """Helps to create a CreditCard instance."""
        self.__creditcard = CreditCard(cardholder="UserTest Name", number="1234123412341234", cvc="123",
                                       valid_until=dt.datetime(year=2032, month=4, day=1), user=UserBuilder().build())

    def with_alias(self, new_alias: str) -> "CreditCardBuilder":
        self.__creditcard.alias = new_alias
        return self

    def build(self) -> CreditCard:
        return self.__creditcard


class TestCreditCard(unittest.TestCase):
    def setUp(self) -> None:
        logger.info("Preparing CREDITCARD instance...")

        # Create new instance
        self.creditcard = CreditCardBuilder().build()
        self.number = "1234123412341234"
        self.cvc = "123"

        logger.info("CREDITCARD instance ready for test...")

    def tearDown(self) -> None:
        del self.creditcard

    def test_creditcardExists(self) -> None:
        self.log_instance(self.creditcard)
        self.assertIsNotNone(self.creditcard, msg="CREDITCARD instance doesn't exists.")
        logger.info(">>> Confirm if CREDITCARD exists...   OK")

    def test_creditcardType(self) -> None:
        self.assertIsInstance(self.creditcard, CreditCard, msg="Creditcard MUST BE creditcard type.")
        logger.info(">>> Confirm if CREDITCARD is instance of CREDITCARD...   OK")

    def test_creditcardUserExists(self) -> None:
        self.assertIsNotNone(self.creditcard.user, msg="Creditcard MUS HAVE an user.")
        logger.info(">>> Confirm if CREDITCARD has USER...   OK")

    def test_creditcardUserType(self) -> None:
        self.assertIsInstance(self.creditcard.user, User, msg="Creditcard user MUST BE user type.")
        logger.info(">>> Confirm if CREDITCARD USER is instance of USER...   OK")

    def test_creditcardCardholderExists(self) -> None:
        self.assertIsNotNone(self.creditcard.cardholder, msg="Creditcard MUST HAVE cardholder.")
        logger.info(">>> Confirm if CREDITCARD has CARDHOLDER...   OK")

    def test_creditcardCardholderType(self) -> None:
        self.assertIsInstance(self.creditcard.cardholder, str, msg="Creditcard cardholder MUST BE string type.")
        logger.info(">>> Confirm if CREDITCARD CARDHOLDER is instance of STRING...   OK")

    def test_creditcardNumberExists(self) -> None:
        self.assertIsNotNone(self.creditcard.encrypted_number, msg="Creditcard MUST HAVE number.")
        logger.info(">>> Confirm if CREDITCARD has NUMBER...   OK")

    def test_creditcardNumberEncrypted(self) -> None:
        self.assertEqual(self.number, decrypt_data(self.creditcard.encrypted_number), msg="Creditcard number MUST BE "
                                                                                          "equal.")
        logger.info(">>> Confirm if CREDITCARD NUMBER is ENCRYPTED...   OK")

    def test_creditcardCVCExists(self) -> None:
        self.assertIsNotNone(self.creditcard.encrypted_cvc, msg="Creditcard MUST HAVE cvc.")
        logger.info(">>> Confirm if CREDITCARD has CVC...   OK")

    def test_creditcardCVCType(self) -> None:
        self.assertIsInstance(self.creditcard.encrypted_cvc, str, msg="Creditcard cvc MUST BE string type.")
        logger.info(">>> Confirm if CREDITCARD CVC is instance of STRING...   OK")

    def test_creditcardCVCEncrypted(self) -> None:
        self.assertEqual(self.cvc, decrypt_data(self.creditcard.encrypted_cvc), msg="Creditcard cvc MUST BE equal.")
        logger.info(">>> Confirm if CREDITCARD CVC is ENCRYPTED...   OK")

    def test_creditcardDateExists(self) -> None:
        self.assertIsNotNone(self.creditcard.valid_until, msg="Creditcard MUST HAVE expires date.")
        logger.info(">>> Confirm if CREDITCARD has EXPIRES DATE...   OK")

    def test_creditcardDateType(self) -> None:
        self.assertIsInstance(self.creditcard.valid_until, dt.datetime, msg="Creditcard date MUST BE datetime type.")
        logger.info(">>> Confirm if CREDITCARD CVC is instance of DATETIME...   OK")

    def test_creditcardAliasType(self) -> None:
        if self.creditcard.alias is not None:
            self.assertIsInstance(self.creditcard.alias, str, msg="Creditcard alias MUST BE none | string type.")
            logger.info(">>> Confirm if CREDITCARD CARD is instance of STRING...   OK")
            return
        self.assertIsInstance(self.creditcard.alias, NoneType, msg="Creditcard alias MUST BE none | string type.")
        logger.info(">>> Confirm if CREDITCARD ALIAS is instance of NONE...   OK")

    @staticmethod
    def log_instance(creditcard: CreditCard) -> None:
        logger.debug(creditcard)


if __name__ == "__main__":
    unittest.main()
