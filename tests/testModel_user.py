import unittest
from hashlib import sha256

from features.models.user import User, UserRole

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


class TestUser(unittest.TestCase):
    def setUp(self) -> None:
        logger.info("Preparing USER instance...")

        # Create new instance
        self.user = UserBuilder().with_role(UserRole.ADMIN).build()
        self.hashed_password = sha256("User_1234".encode()).hexdigest()

        logger.info("USER instances ready for test...")

    def tearDown(self) -> None:
        del self.user

    def test_userExists(self) -> None:
        self.log_instance(self.user)
        self.assertIsNotNone(self.user, msg="USER instance doesn't exist.")
        logger.info(">>> Confirm if USER exists...   OK")

    def test_userType(self) -> None:
        self.assertIsInstance(self.user, User, msg="User MUST BE a user type.")
        logger.info(">>> Confirm if USER is instance of USER...   OK")

    def test_userFullnameExists(self) -> None:
        self.assertIsNotNone(self.user.fullname, msg="User MUST HAVE fullname.")
        logger.info(">>> Confirm if USER has FULLNAME...   OK")

    def test_userFullnameType(self) -> None:
        self.assertIsInstance(self.user.fullname, str, msg="Fullname MUST BE string type.")
        logger.info(">>> Confirm if USER NAME is instance of STRING...   OK")

    def test_userPasswordExists(self) -> None:
        self.assertIsNotNone(self.user.hashed_password, msg="User MUST HAVE password.")
        logger.info(">>> Confirm if USER has PASSWORD...   OK")

    def test_userPasswordType(self) -> None:
        self.assertIsInstance(self.user.hashed_password, str, msg="Password MUST BE string type.")
        logger.info(">>> Confirm if USER PASSWORD is instance of STRING...   OK")

    def test_userPasswordHashed(self):
        self.assertEqual(self.user.hashed_password, self.hashed_password, msg="Password MUST BE hashed.")
        logger.info(">>> Confirm if PASSWORD is HASHED...   OK")

    def test_userRole(self) -> None:
        self.assertEqual(self.user.role, UserRole.ADMIN, msg="Role must be ADMIN.")

    @staticmethod
    def log_instance(user: User) -> None:
        logger.debug(user)


if __name__ == "__main__":
    unittest.main()
