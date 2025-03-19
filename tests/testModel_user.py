import unittest
from hashlib import sha256

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


class TestUser(unittest.TestCase):
    def setUp(self) -> None:
        log.info("Preparing USER instance...")

        # Create new instance
        self.user = UserBuilder().with_role(UserRole.ADMIN).build()
        self.hashed_password = sha256(b"User_1234").hexdigest()

        log.info("USER instances ready for test...")

    def tearDown(self) -> None:
        del self.user

    def test_userExists(self) -> None:
        self.log_instance(self.user)
        self.assertIsNotNone(
            obj=self.user,
            msg="USER instance doesn't exist."
        )
        log.info(">>> Confirm if USER exists...   OK")

    def test_userType(self) -> None:
        self.assertIsInstance(
            obj=self.user,
            cls=User,
            msg="User MUST BE a user type."
        )
        log.info(">>> Confirm if USER is instance of USER...   OK")

    def test_userFullnameExists(self) -> None:
        self.assertIsNotNone(
            obj=self.user.fullname,
            msg="User MUST HAVE fullname."
        )
        log.info(">>> Confirm if USER has FULLNAME...   OK")

    def test_userFullnameType(self) -> None:
        self.assertIsInstance(
            obj=self.user.fullname,
            cls=str,
            msg="Fullname MUST BE string type."
        )
        log.info(">>> Confirm if USER NAME is instance of STRING...   OK")

    def test_userEmailExists(self) -> None:
        self.assertIsNotNone(
            obj=self.user.email,
            msg="User MUST HAVE email."
        )
        log.info(">>> Confirm if USER has EMAIL...   OK")

    def test_userEmailType(self) -> None:
        self.assertIsInstance(
            obj=self.user.email,
            cls=str,
            msg="Email MUST BE a string type."
        )
        log.info(">>> Confirm if EMAIL is instance of STRING...   OK")

    def test_userPasswordExists(self) -> None:
        self.assertIsNotNone(
            obj=self.user.hashed_password,
            msg="User MUST HAVE password."
        )
        log.info(">>> Confirm if USER has PASSWORD...   OK")

    def test_userPasswordType(self) -> None:
        self.assertIsInstance(
            obj=self.user.hashed_password,
            cls=str,
            msg="Password MUST BE string type."
        )
        log.info(">>> Confirm if USER PASSWORD is instance of STRING...   OK")

    def test_userPasswordHashed(self):
        self.assertEqual(
            first=self.user.hashed_password,
            second=self.hashed_password,
            msg="Password MUST BE hashed."
        )
        log.info(">>> Confirm if PASSWORD is HASHED...   OK")

    def test_userRoleExists(self) -> None:
        self.assertIsNotNone(
            obj=self.user.role,
            msg="User MUST HAVE role."
        )
        log.info(">>> Confirm if USER has ROLE...   OK")

    def test_userRoleType(self) -> None:
        self.assertIsInstance(
            obj=self.user.role,
            cls=UserRole,
            msg="Role MUST BE a user_role type."
        )
        log.info(">>> Confirm if USER has ROLE...   OK")

    def test_userRole(self) -> None:
        self.assertEqual(
            first=self.user.role,
            second=UserRole.ADMIN,
            msg="Role must be ADMIN."
        )
        log.info(">>> Confirm if USER ROLE is ADMIN...   OK")

    @staticmethod
    def log_instance(user: User) -> None:
        log.debug(user)


if __name__ == "__main__":
    unittest.main()
