import unittest

from features.data_encryption.core import decrypt_data, encrypt_data
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
        self.__request = PasswordRequest(user=UserBuilder().build())

    def build(self) -> PasswordRequest:
        return self.__request


class TestPasswordRequest(unittest.TestCase):
    def setUp(self) -> None:
        log.info("Preparing PASSWORD REQUEST instance...")

        # Create new instance
        self.request = PasswordRequestBuilder().build()
        self.code_length = encrypt_data("ABC1234")

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

    def test_passwordRequestEncryptedCodeExists(self) -> None:
        self.assertIsNotNone(
            obj=self.request.encrypted_code,
            msg="Password request MUST HAVE encrypted code."
        )
        log.info(">>> Confirm if PASSWORD REQUEST has CODE ENCRYPTED...   OK")

    def test_passwordRequestCodeIsEncrypt(self) -> None:
        self.assertEqual(
            first=len(self.code_length),
            second=len(self.request.encrypted_code),
            msg="Password request code MUST BE encrypted."
        )
        log.info(">>> Confirm if PASSWORD REQUEST CODE is ENCRYPTED...   OK")

    def test_passwordRequestEncryptedCodeType(self) -> None:
        self.assertIsInstance(
            obj=self.request.encrypted_code,
            cls=str,
            msg="Password request code MUST BE string type."
        )
        log.info(">>> Confirm if PASSWORD REQUEST ENCRYPTED CODE is instance of STRING...   OK")

    def test_passwordRequestDecryptedCodeExists(self) -> None:
        self.assertIsNotNone(
            obj=decrypt_data(self.request.encrypted_code),
            msg="Password request MUST HAVE decrypted code."
        )
        log.info(">>> Confirm if PASSWORD REQUEST has CODE DECRYPTED...   OK")

    def test_passwordRequestCodeDecrypt(self) -> None:
        self.assertEqual(
            first=len(decrypt_data(self.code_length)),
            second=len(decrypt_data(self.request.encrypted_code)),
            msg="Password request code MUST BE decrypted (length=7)."
        )
        log.info(">>> Confirm if PASSWORD REQUEST CODE is DECRYPTED...   OK")

    def test_passwordRequestDecryptedCodeType(self) -> None:
        self.assertIsInstance(
            obj=decrypt_data(self.request.encrypted_code),
            cls=str,
            msg="Password request code MUST BE string type."
        )
        log.info(">>> Confirm if PASSWORD REQUEST DECRYPTED CODE is instance of STRING...   OK")

    @staticmethod
    def log_instance(request: PasswordRequest) -> None:
        log.debug(request)


if __name__ == "__main__":
    unittest.main()
