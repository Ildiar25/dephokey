import unittest

from features.models.user import User, UserRole
from features.email_management.create_email import CreateEmail

from shared.logger_setup import test_logger as logger


class UserBuilder:
    def __init__(self) -> None:
        """Helps to create a User instance."""
        self.__user = User(fullname="User Test Name", email="user.email@example.com", password="User_1234")

    def with_role(self, new_role: UserRole) -> "UserBuilder":
        self.__user.role = new_role
        return self

    def build(self) -> User:
        return self.__user


class TestCreateEmail(unittest.TestCase):
    def setUp(self) -> None:
        logger.info("Preparing CREATE EMAIL instance...")

        # Create comparable items
        self.name = "User"
        self.user_email = "user.email@example.com"
        self.code = "ABC1234"
        self.text_plain = ("Hola User!\nPor favor, introduce en el programa el código de siete caracteres "
                           "proporcionado\npara poder actualizar tu contraseña:\n\nABC1234\n\nSi no has "
                           "realizado la petición, puedes ignorar este email.\n\nAtentamente,\nEl equipo Dephokey")
        self.html_message = ('<!DOCTYPE html>\n<html lang="es">\n\n<head>\n    <meta charset="UTF-8">\n    '
                             '<meta name="viewport" content="width=device-width,initial-scale=1.0">\n    <style>'
                             '\n        body {background-color: #F2F2F2; text-align: center; font-family: Arial, '
                             'Helvetica, sans-serif}\n        h1 {margin: 1rem 0; color: #4860B5}\n        td '
                             '{padding-top: 40px}\n        p {padding-bottom: 16px}\n\n        .main-table-position '
                             '{\n            max-width: 500px; border-collapse: collapse; border: 0px; border-spacing: '
                             '0px;\n            margin-left: auto; margin-right: auto; text-align: left\n        }'
                             '\n        .left-align {text-align: left}\n        .center-align {text-align: center}\n'
                             '        .footer {padding-top: 5px; color: #9A9A9A; text-align: center}\n        '
                             '.content-design {padding: 20px; background-color: #FFFFFF; border-radius: 4px}\n\n'
                             '        #code {color: #0E2060}\n        #main-content {color: #333333}\n        '
                             '#logotype {padding-bottom: 10px}\n    </style>\n    <title></title>\n</head>\n\n<body>\n'
                             '    <table class="main-table-position" role="presentation">\n        <tbody>\n'
                             '            <tr>\n                <td>\n                    <!-- Logotype -->\n'
                             '                    <div class="left-align">\n                        '
                             '<div id="logotype">\n                            <img src="assets/logotype.svg" '
                             'alt="logo dephokey" style="width: 120px">\n                        </div>\n'
                             '                    </div>\n                    <!-- Body content -->\n'
                             '                    <div class="content-design">\n                        '
                             '<div id="main-content" class="left-align">\n                            <h1>Código de '
                             'Verificación</h1>\n                            <p>Hola User!<br>Por favor, introduce '
                             'en el programa\n                                el código de siete caracteres '
                             'proporcionado para poder actualizar tu contraseña:</p>\n                            '
                             '<p id="code" class="center-align">\n                                    '
                             '<strong style="font-size: 180%;">ABC1234</strong></p>\n                            '
                             '<p>Si no has realizado la petición, puedes ignorar este email.</p>\n'
                             '                            <p>Atentamente,<br>El equipo Dephokey</p>\n'
                             '                        </div>\n                    </div>\n                    '
                             '<div class="footer">\n                        <p>DephoKey © 2025 · Todos los derechos '
                             'reservados </p>\n                    </div>\n                </td>\n            </tr>\n'
                             '        </tbody>\n    </table>\n</body>\n\n</html>')

        # Create new instance
        self.email = CreateEmail(UserBuilder().build(), code="ABC1234")

        logger.info("CREATE EMAIL ready for test...")

    def tearDown(self) -> None:
        del self.email

    def test_createEmailExists(self) -> None:
        self.log_instance(self.email)
        self.assertIsNotNone(self.email, msg="CREATE EMAIL instance doesn't exist.")
        logger.info(">>> Confirm if CREATE EMAIL exists...   OK")

    def test_createEmailType(self) -> None:
        self.assertIsInstance(self.email, CreateEmail, msg="Create email MUST BE create email type.")
        logger.info(">>> Confirm if CREATE EMAIL is instance of CREATE EMAIL...   OK")

    def test_createEmailNameExists(self) -> None:
        self.assertIsNotNone(self.email.name, msg="Create email MUST HAVE name.")
        logger.info(">>> Confirm if CREATE EMAIL has NAME...   OK")

    def test_createEmailNameType(self) -> None:
        self.assertIsInstance(self.email.name, str, msg="Name MUST BE string type.")
        logger.info(">>> Confirm if NAME is instance of STRING...   OK")

    def test_createEmailNameComparison(self) -> None:
        self.assertEqual(self.name, self.email.name, msg="Name content MUST BE equal.")
        logger.info(">>> Confirm if NAME is setted right...   OK")

    def test_createEmailUseremailExists(self) -> None:
        self.assertIsNotNone(self.email.receiver, msg="Create email MUST HAVE email.")
        logger.info(">>> Confirm if CREATE EMAIL has EMAIL...   OK")

    def test_createEmailUseremailType(self) -> None:
        self.assertIsInstance(self.email.receiver, str, msg="Email MUST BE string type.")
        logger.info(">>> Confirm if EMAIL is instance of STRING...   OK")

    def test_createEmailUseremailComparison(self) -> None:
        self.assertEqual(self.user_email, self.email.receiver, msg="Email content MUST BE equal.")
        logger.info(">>> Confirm if EMAIL is setted right...   OK")

    def test_createEmailCodeExists(self) -> None:
        self.assertIsNotNone(self.email.code, msg="Create email MUST HAVE code.")
        logger.info(">>> Confirm if CREATE EMAIL has CODE...   OK")

    def test_createEmailCodeType(self) -> None:
        self.assertIsInstance(self.email.code, str, msg="Code MUST BE string type.")
        logger.info(">>> Confirm if CODE is instance of STRING...   OK")

    def test_createEmailCodeLenght(self) -> None:
        self.assertEqual(first=len(self.email.code), second=7, msg="Code lenght MUST BE 7 characters.")
        logger.info(">>> Confirm if CODE LENGTH is VALID...   OK")

    def test_createEmailMessageExists(self) -> None:
        self.assertIsNotNone(self.email.message_content, msg="Create email MUST HAVE content.")
        logger.info(">>> Confirm if CREATE EMAIL has CONTENT...   OK")

    def test_createEmailMessateType(self) -> None:
        self.assertIsInstance(self.email.message_content, tuple, msg="Content MUST BE tuple type.")
        logger.info(">>> Confirm if CONTENT is instance of TUPLE...   OK")

    def test_createEmailMessageTextComparison(self) -> None:
        self.assertEqual(self.text_plain, self.email.message_content[0],
                         msg="Text plain content MUST BE equal.")
        logger.info(">>> Confirm if TEXT PLAIN is EQUAL...   OK")

    def test_createEmailMessageHTMLComparison(self) -> None:
        if self.email.message_content[1] is not None:
            self.assertEqual(self.html_message, self.email.message_content[1],
                             msg="HTML content MUST BE equal.")
            logger.info(">>> Confirm EMAIL CONTENT has HTML...   OK")
            return
        self.assertIsNone(self.email.message_content[1], msg="Content MUST BE None type.")
        logger.info(">>> Confirm EMAIL CONTENT hasn't HTML...   OK")

    @staticmethod
    def log_instance(email: CreateEmail) -> None:
        logger.debug(email)


if __name__ == "__main__":
    unittest.main()
