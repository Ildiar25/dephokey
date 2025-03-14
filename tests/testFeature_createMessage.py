import unittest

from features.models.user import User, UserRole
from features.email_management.create_message import CreateMessage, MessageStyle

from shared.logger_setup import test_log as log


class UserBuilder:
    def __init__(self) -> None:
        """Helps to create a User instance."""
        self.__user = User(fullname="User Test Name", email="user.email@example.com", password="User_1234")

    def with_role(self, new_role: UserRole) -> "UserBuilder":
        self.__user.role = new_role
        return self

    def build(self) -> User:
        return self.__user


class TestCreateMessage(unittest.TestCase):
    def setUp(self) -> None:
        log.info("Preparing CREATE MESSAGE instance...")

        # Create comparable items
        self.name = "User Test Name"
        self.code = "ABC1234"
        self.text = ("Hola User Test Name!\nPor favor, introduce en el programa el código de siete caracteres "
                           "proporcionado\npara poder actualizar tu contraseña:\n\nABC1234\n\nSi no has "
                           "realizado la petición, puedes ignorar este email.\n\nAtentamente,\nEl equipo Dephokey")

        # Create new instance
        self.message = CreateMessage(
            MessageStyle.RESET,
            send_to=UserBuilder().build().email,
            name=UserBuilder().build().fullname,
            token="ABC1234"
        ).create()

        log.info("CREATE MESSAGE ready for test...")

    def tearDown(self) -> None:
        del self.message

    def test_createMessageExists(self) -> None:
        self.log_instance(self.message)
        self.assertIsNotNone(self.message, msg="CREATE MESSAGE instance doesn't exist.")
        log.info(">>> Confirm if CREATE MESSAGE exists...   OK")

    def test_createMessageType(self) -> None:
        self.assertIsInstance(self.message, CreateMessage, msg="Create message MUST BE create message type.")
        log.info(">>> Confirm if CREATE MESSAGE is instance of CREATE MESSAGE...   OK")

    def test_createMessageNameExists(self) -> None:
        self.assertIsNotNone(self.message.name, msg="Create message MUST HAVE name.")
        log.info(">>> Confirm if CREATE MESSAGE has NAME...   OK")

    def test_createMessageNameType(self) -> None:
        self.assertIsInstance(self.message.name, str, msg="Name MUST BE string type.")
        log.info(">>> Confirm if NAME is instance of STRING...   OK")

    def test_createMessageNameComparison(self) -> None:
        self.assertEqual(self.name, self.message.name, msg="Name content MUST BE equal.")
        log.info(">>> Confirm if NAME is setted right...   OK")

    def test_createMessageTokenExists(self) -> None:
        self.assertIsNotNone(self.message.token, msg="Create message MUST HAVE token.")
        log.info(">>> Confirm if CREATE MESSAGE has TOKEN...   OK")

    def test_createMessageTokenType(self) -> None:
        self.assertIsInstance(self.message.token, str, msg="Token MUST BE string type.")
        log.info(">>> Confirm if TOKEN is instance of STRING...   OK")

    def test_createMessageTokenLenght(self) -> None:
        self.assertEqual(first=len(self.message.token), second=7, msg="Token lenght MUST BE 7 characters.")
        log.info(">>> Confirm if TOKEN LENGTH is VALID...   OK")

    def test_createMessageTextMessageExists(self) -> None:
        self.assertIsNotNone(self.message.with_text, msg="Create message MUST HAVE text content.")
        log.info(">>> Confirm if CREATE MESSAGE has TEXT CONTENT...   OK")

    def test_createMessageTextMessateType(self) -> None:
        self.assertIsInstance(self.message.with_text, str, msg="Text message MUST BE string type.")
        log.info(">>> Confirm if TEXT CONTENT is instance of STRING...   OK")

    def test_createMessageTextMessageComparison(self) -> None:
        self.assertEqual(self.text, self.message.with_text, msg="Text plain content MUST BE equal.")
        log.info(">>> Confirm if TEXT PLAIN is EQUAL...   OK")

    @staticmethod
    def log_instance(email: CreateMessage) -> None:
        log.debug(email.__str__())


if __name__ == "__main__":
    unittest.main()
