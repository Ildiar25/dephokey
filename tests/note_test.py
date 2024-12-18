import unittest

from features.models.user import User
from features.models.note import Note

from shared.logger_setup import test_logger as logger


class TestNote(unittest.TestCase):
    def setUp(self) -> None:
        logger.info("Preparing NOTE instances...")

        self.user_test = User("admin", "admin@admin.com", "admin1234")

        # Create new instances
        self.note_01 = Note("TestContent", self.user_test)
        self.note_02 = Note("TestContent", self.user_test, "Test02")

        logger.info("NOTE instances ready for test...")

    def tearDown(self) -> None:
        logger.info("Finishing NOTE test...")

    def test_print_instance(self) -> None:
        logger.debug(self.note_01)
        logger.debug(self.note_02)

    def test_note_fields(self) -> None:
        logger.info(">>> Starting NOTE fields test...")
        self.assertEqual(self.note_01.title, None, "Should be 'None'...")
        self.assertEqual(self.note_02.title, "Test02", "Should be 'Test02'...")
        self.assertEqual(self.note_01.user, self.user_test, "Should be 'user_test'...")
