import unittest

from features.models.user import User
from features.models.note import Note

from shared.logger_setup import test_logger as logger


class TestNote(unittest.TestCase):
    def test_create_instance(self) -> None:
        logger.info("Starting test note...")

        user_test = User("admin", "admin@admin.com", "admin1234")

        # Create new instances
        note_01 = Note("TestContent", user_test)
        note_02 = Note("TestContent", user_test, "Test02")
        self.assertEqual(note_01.title, None, "Should be None")
        self.assertEqual(note_02.title, "Test02", "Should be Test02")

        # Register instance
        logger.debug(note_01)
        logger.debug(note_02)

        # Finish test
        logger.info("Ending test note...")
