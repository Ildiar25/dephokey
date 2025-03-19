import datetime
import unittest
from datetime import timedelta
from types import NoneType

from features.data_encryption.core import decrypt_data
from features.models.creditcard import CreditCard
from features.models.user import User, UserRole
from shared.logger_setup import test_log as log


class UserBuilder:
    def __init__(self) -> None:
        """Helps to create a User instance."""
        self.__user = User(
            fullname="UserTest Name",
            email="user.email@example.com",
            password="User_1234"
        )

    def with_role(self, new_role: UserRole) -> "UserBuilder":
        self.__user.role = new_role
        return self

    def build(self) -> User:
        return self.__user


class CreditCardBuilder:
    def __init__(self) -> None:
        """Helps to create a CreditCard instance."""
        self.__creditcard = CreditCard(
            cardholder="UserTest Name",
            number="1234123412341234",
            cvc="123",
            valid_until=datetime.datetime.today() + timedelta(weeks=260),
            user=UserBuilder().build()
        )

    def with_alias(self, new_alias: str) -> "CreditCardBuilder":
        self.__creditcard.alias = new_alias
        return self

    def build(self) -> CreditCard:
        return self.__creditcard


class TestCreditCard(unittest.TestCase):
    def setUp(self) -> None:
        log.info("Preparing CREDITCARD instance...")

        # Create new instance
        self.creditcard = CreditCardBuilder().build()
        self.number = "1234123412341234"
        self.cvc = "123"

        log.info("CREDITCARD instance ready for test...")

    def tearDown(self) -> None:
        del self.creditcard

    def test_creditcardExists(self) -> None:
        self.log_instance(self.creditcard)
        self.assertIsNotNone(
            obj=self.creditcard,
            msg="CREDITCARD instance doesn't exists."
        )
        log.info(">>> Confirm if CREDITCARD exists...   OK")

    def test_creditcardType(self) -> None:
        self.assertIsInstance(
            obj=self.creditcard,
            cls=CreditCard,
            msg="Creditcard MUST BE creditcard type."
        )
        log.info(">>> Confirm if CREDITCARD is instance of CREDITCARD...   OK")

    def test_creditcardUserExists(self) -> None:
        self.assertIsNotNone(
            obj=self.creditcard.user,
            msg="Creditcard MUS HAVE an user."
        )
        log.info(">>> Confirm if CREDITCARD has USER...   OK")

    def test_creditcardUserType(self) -> None:
        self.assertIsInstance(
            obj=self.creditcard.user,
            cls=User,
            msg="Creditcard user MUST BE user type."
        )
        log.info(">>> Confirm if CREDITCARD USER is instance of USER...   OK")

    def test_creditcardCardholderExists(self) -> None:
        self.assertIsNotNone(
            obj=self.creditcard.cardholder,
            msg="Creditcard MUST HAVE cardholder."
        )
        log.info(">>> Confirm if CREDITCARD has CARDHOLDER...   OK")

    def test_creditcardCardholderType(self) -> None:
        self.assertIsInstance(
            obj=self.creditcard.cardholder,
            cls=str,
            msg="Creditcard cardholder MUST BE string type."
        )
        log.info(">>> Confirm if CREDITCARD CARDHOLDER is instance of STRING...   OK")

    def test_creditcardNumberExists(self) -> None:
        self.assertIsNotNone(
            obj=self.creditcard.encrypted_number,
            msg="Creditcard MUST HAVE number."
        )
        log.info(">>> Confirm if CREDITCARD has NUMBER...   OK")

    def test_creditcardNumberType(self) -> None:
        self.assertIsInstance(
            obj=self.creditcard.encrypted_number,
            cls=str,
            msg="Creditcard number MUST BE string type."
        )
        log.info(">>> Confirm if CREDITCARD NUMBER is instance of STRING...   OK")

    def test_creditcardNumberEncrypted(self) -> None:
        self.assertEqual(
            first=self.number,
            second=decrypt_data(self.creditcard.encrypted_number),
            msg="Creditcard number MUST BE encrypted."
        )
        log.info(">>> Confirm if CREDITCARD NUMBER is ENCRYPTED...   OK")

    def test_creditcardCVCExists(self) -> None:
        self.assertIsNotNone(
            obj=self.creditcard.encrypted_cvc,
            msg="Creditcard MUST HAVE cvc."
        )
        log.info(">>> Confirm if CREDITCARD has CVC...   OK")

    def test_creditcardCVCType(self) -> None:
        self.assertIsInstance(
            obj=self.creditcard.encrypted_cvc,
            cls=str,
            msg="Creditcard cvc MUST BE string type."
        )
        log.info(">>> Confirm if CREDITCARD CVC is instance of STRING...   OK")

    def test_creditcardCVCEncrypted(self) -> None:
        self.assertEqual(
            first=self.cvc,
            second=decrypt_data(self.creditcard.encrypted_cvc),
            msg="Creditcard cvc MUST BE encrypted."
        )
        log.info(">>> Confirm if CREDITCARD CVC is ENCRYPTED...   OK")

    def test_creditcardDateExists(self) -> None:
        self.assertIsNotNone(
            obj=self.creditcard.valid_until,
            msg="Creditcard MUST HAVE expires date."
        )
        log.info(">>> Confirm if CREDITCARD has EXPIRES DATE...   OK")

    def test_creditcardDateType(self) -> None:
        self.assertIsInstance(
            obj=self.creditcard.valid_until,
            cls=datetime.datetime,
            msg="Creditcard date MUST BE datetime type."
        )
        log.info(">>> Confirm if CREDITCARD CVC is instance of DATETIME...   OK")

    def test_creditcardDateIsNotExpired(self) -> None:
        self.assertGreater(
            a=self.creditcard.valid_until,
            b=datetime.datetime.today(),
            msg="Creditcard date MUST BE less than TODAY."
        )
        log.info(">>> Confirm if CREDITCARD DATE is not EXPIRED...   OK")

    def test_creditcardAliasType(self) -> None:
        if self.creditcard.alias is not None:
            self.assertIsInstance(
                obj=self.creditcard.alias,
                cls=str,
                msg="Creditcard alias MUST BE none | string type."
            )
            log.info(">>> Confirm if CREDITCARD CARD is instance of STRING...   OK")
            return

        self.assertIsInstance(
            obj=self.creditcard.alias,
            cls=NoneType,
            msg="Creditcard alias MUST BE none | string type."
        )
        log.info(">>> Confirm if CREDITCARD ALIAS is instance of NONE...   OK")

    @staticmethod
    def log_instance(creditcard: CreditCard) -> None:
        log.debug(creditcard)


if __name__ == "__main__":
    unittest.main()
