import unittest

from features.email_management.create_message import MessageStyle
from features.email_management.send_email import SendEmail
from features.models.user import User, UserRole
from shared.logger_setup import test_log as log


class UserBuilder:
    def __init__(self) -> None:
        """Helps to create a User instance."""
        self.__user = User(
            fullname="User Test Name",
            email="user.email@example.com",
            password="User_1234"
        )

    def with_role(self, new_role: UserRole) -> "UserBuilder":
        self.__user.role = new_role
        return self

    def build(self) -> User:
        return self.__user


class TestSendEmail(unittest.TestCase):
    def setUp(self) -> None:
        log.info("Preparing SEND EMAIL instance...")

        # Create needed elements
        self.token = "ABC1234"

        # Create send email instance
        self.email = SendEmail(
            msg_style=MessageStyle.RESET,
            send_to=UserBuilder().build().email,
            name=UserBuilder().build().fullname,
            token=self.token
        )

    def tearDown(self) -> None:
        del self.email

    def test_sendEmailExists(self) -> None:
        self.log_instance(self.email)
        self.assertIsNotNone(
            obj=self.email,
            msg="SEND EMAIL instance doesn't exist."
        )
        log.info(">>> Confirm if SEND MESSAGE exists...   OK")

    def test_sendEmailType(self) -> None:
        self.assertIsInstance(
            obj=self.email,
            cls=SendEmail,
            msg="Send email MUST BE send email type."
        )
        log.info(">>> Confirm if SEND EMAIL is instance of SEND EMAIL...   OK")

    def test_sendEmailSend(self) -> None:
        success = self.email.send()
        self.assertTrue(
            expr=success,
            msg="SEND EMAIL doesn't send the email (Docker Server must be started before execute this test). "
        )
        log.info(">>> Confirm if SEND EMAIL has sent the EMAIL...   OK")

    @staticmethod
    def log_instance(email: SendEmail) -> None:
        log.debug(email)


if __name__ == "__main__":
    unittest.main()
