import unittest
from types import NoneType

from features.data_encryption.core import decrypt_data
from features.models.user import User, UserRole
from features.models.note import Note

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


class NoteBuilder:
    def __init__(self) -> None:
        """Helps to create Note instance."""
        self.__note = Note(title=None, content="Testing Note content...", user=UserBuilder().build())

    def with_title(self, new_title: str) -> "NoteBuilder":
        self.__note.title = new_title
        return self

    def build(self) -> Note:
        return self.__note


class TestNote(unittest.TestCase):
    def setUp(self) -> None:
        logger.info("Preparing NOTE instance...")

        # Create new instance
        self.note = NoteBuilder().build()
        self.content = "Testing Note content..."

        logger.info("NOTE instance ready for test...")

    def tearDown(self) -> None:
        del self.note

    def test_noteExists(self) -> None:
        self.log_instance(self.note)
        self.assertIsNotNone(self.note, msg="NOTE instance doesn't exists.")
        logger.info(">>> Confirm if NOTE exists...   OK")

    def test_noteType(self) -> None:
        self.assertIsInstance(self.note, Note, msg="Note MUST BE note type.")
        logger.info(">>> Confirm if NOTE is instance of NOTE...   OK")

    def test_noteUserExists(self) -> None:
        self.assertIsNotNone(self.note.user, msg="Note MUS HAVE an user.")
        logger.info(">>> Confirm if NOTE has USER...   OK")

    def test_noteUserType(self) -> None:
        self.assertIsInstance(self.note.user, User, msg="Note user MUST BE user type.")
        logger.info(">>> Confirm if NOTE USER is instance of USER...   OK")

    def test_noteTitleType(self) -> None:
        if self.note.title is not None:
            self.assertIsInstance(self.note.title, str, msg="Note title MUST BE none | string type.")
            logger.info(">>> Confirm if NOTE TITLE is instance of STRING...   OK")
            return
        self.assertIsInstance(self.note.title, NoneType, msg="Note title MUST BE none | string type.")
        logger.info(">>> Confirm if NOTE TITLE is instance of NONE...   OK")

    def test_contentExists(self) -> None:
        self.assertIsNotNone(self.content, msg="Note MUST HAVE content.")
        logger.info(">>> Confirm if NOTE has CONTENT...   OK")

    def test_contentType(self) -> None:
        self.assertIsInstance(self.content, str, msg="Note content MUST BE string type.")
        logger.info(">>> Confirm if NOTE CONTENT is instance of STRING...   OK")

    def test_noteContentEncrypted(self) -> None:
        self.assertEqual(self.content, decrypt_data(self.note.encrypted_content), msg="Note content MUST BE equal.")
        logger.info(">>> Confirm if NOTE CONTENT is ENCRYPTED...   OK")

    @staticmethod
    def log_instance(note: Note) -> None:
        logger.debug(note)


if __name__ == "__main__":
    unittest.main()
