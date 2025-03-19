import unittest

from features.data_encryption.core import decrypt_data
from features.models.password_request import PasswordRequest
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


class PasswordRequestBuilder:
    def __init__(self) -> None:
        """Helps to create PasswordRequest instance."""
        self.__request = PasswordRequest(
            code="ABC1234",
            user=UserBuilder().build()
        )

    def build(self) -> PasswordRequest:
        return self.__request


class TestPasswordRequest(unittest.TestCase):
    def setUp(self) -> None:
        log.info("Preparing PASSWORD REQUEST instance...")

        # Create new instance
        self.request = PasswordRequestBuilder().build()
        self.code = "ABC1234"

        log.info("PASSWORD REQUEST instance ready for test...")

    def tearDown(self) -> None:
        del self.request

    def test_passwordRequestExists(self) -> None:
        self.log_instance(self.request)
        self.assertIsNotNone(
            obj=self.request,
            msg="PASSWORD REQUEST instance doesn't exists."
        )
        log.info(">>> Confirm if PASSWORD REQUEST exists...   OK")

    def test_passwordRequestType(self) -> None:
        self.assertIsInstance(
            obj=self.request,
            cls=PasswordRequest,
            msg="Password request MUST BE password request type."
        )
        log.info(">>> Confirm if PASSWORD REQUEST is instance of PASSWORD REQUEST...   OK")

    def test_passwordRequestUserExists(self) -> None:
        self.assertIsNotNone(
            obj=self.request.user,
            msg="Password request MUS HAVE an user."
        )
        log.info(">>> Confirm if PASSWORD REQUEST has USER...   OK")

    def test_passwordRequestUserType(self) -> None:
        self.assertIsInstance(
            obj=self.request.user,
            cls=User,
            msg="Password request user MUST BE user type."
        )
        log.info(">>> Confirm if PASSWORD REQUEST USER is instance of USER...   OK")

    def test_passwordRequestCodeExists(self) -> None:
        self.assertIsNotNone(
            obj=self.request.encrypted_code,
            msg="Password request MUST HAVE code."
        )
        log.info(">>> Confirm if PASSWORD REQUEST has CODE...   OK")

    def test_passwordRequestCodeType(self) -> None:
        self.assertIsInstance(
            obj=self.request.encrypted_code,
            cls=str,
            msg="Password request code MUST BE string type."
        )
        log.info(">>> Confirm if PASSWORD REQUEST CODE is instance of STRING...   OK")

    def test_passwordRequestCodeEncrypted(self) -> None:
        self.assertEqual(
            first=self.code,
            second=decrypt_data(self.request.encrypted_code),
            msg="Password request code MUST BE equal."
        )
        log.info(">>> Confirm if PASSWORD REQUEST CODE is ENCRYPTED...   OK")

    @staticmethod
    def log_instance(request: PasswordRequest) -> None:
        log.debug(request)


if __name__ == "__main__":
    unittest.main()
