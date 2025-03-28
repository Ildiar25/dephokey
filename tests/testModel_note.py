import unittest
from types import NoneType

from features.data_encryption.core import decrypt_data
from features.models.note import Note
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


class NoteBuilder:
    def __init__(self) -> None:
        """Helps to create Note instance."""
        self.__note = Note(
            title=None,
            content="Testing Note content...",
            user=UserBuilder().build()
        )

    def with_title(self, new_title: str) -> "NoteBuilder":
        self.__note.title = new_title
        return self

    def build(self) -> Note:
        return self.__note


class TestNote(unittest.TestCase):
    def setUp(self) -> None:
        log.info("Preparing NOTE instance...")

        # Create new instance
        self.note = NoteBuilder().build()
        self.content = "Testing Note content..."

        log.info("NOTE instance ready for test...")

    def tearDown(self) -> None:
        del self.note

    def test_noteExists(self) -> None:
        self.log_instance(self.note)
        self.assertIsNotNone(
            obj=self.note,
            msg="NOTE instance doesn't exists."
        )
        log.info(">>> Confirm if NOTE exists...   OK")

    def test_noteType(self) -> None:
        self.assertIsInstance(
            obj=self.note,
            cls=Note,
            msg="Note MUST BE note type."
        )
        log.info(">>> Confirm if NOTE is instance of NOTE...   OK")

    def test_noteUserExists(self) -> None:
        self.assertIsNotNone(
            obj=self.note.user,
            msg="Note MUS HAVE an user."
        )
        log.info(">>> Confirm if NOTE has USER...   OK")

    def test_noteUserType(self) -> None:
        self.assertIsInstance(
            obj=self.note.user,
            cls=User,
            msg="Note user MUST BE user type."
        )
        log.info(">>> Confirm if NOTE USER is instance of USER...   OK")

    def test_noteTitleType(self) -> None:
        if self.note.title is not None:
            self.assertIsInstance(
                obj=self.note.title,
                cls=str,
                msg="Note title MUST BE none | string type."
            )
            log.info(">>> Confirm if NOTE TITLE is instance of STRING...   OK")
            return

        self.assertIsInstance(
            obj=self.note.title,
            cls=NoneType,
            msg="Note title MUST BE none | string type."
        )
        log.info(">>> Confirm if NOTE TITLE is instance of NONE...   OK")

    def test_contentExists(self) -> None:
        self.assertIsNotNone(
            obj=self.content,
            msg="Note MUST HAVE content."
        )
        log.info(">>> Confirm if NOTE has CONTENT...   OK")

    def test_contentType(self) -> None:
        self.assertIsInstance(
            obj=self.content,
            cls=str,
            msg="Note content MUST BE string type."
        )
        log.info(">>> Confirm if NOTE CONTENT is instance of STRING...   OK")

    def test_noteContentEncrypted(self) -> None:
        self.assertEqual(
            first=self.content,
            second=decrypt_data(self.note.encrypted_content),
            msg="Note content MUST BE equal."
        )
        log.info(">>> Confirm if NOTE CONTENT is ENCRYPTED...   OK")

    @staticmethod
    def log_instance(note: Note) -> None:
        log.debug(note)


if __name__ == "__main__":
    unittest.main()
