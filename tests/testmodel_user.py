import unittest
from hashlib import sha256

from features.models.user import User, UserRole

from shared.logger_setup import test_logger as logger


class TestUser(unittest.TestCase):
    def setUp(self) -> None:
        logger.info("Preparing USER instances...")

        # Create new instances
        self.user_01 = User("Administrador", "admin.24@gmail.com", "admin1234", UserRole.ADMIN)
        self.user_02 = User("Cliente", "client.24@gmail.com", "client1234")
        self.hashed_password = sha256("admin1234".encode()).hexdigest()

        logger.info("USER instances ready for test...")

    def tearDown(self) -> None:
        logger.info("Finishing USER test...")

    def test_print_instance(self) -> None:
        logger.debug(self.user_01)
        logger.debug(self.user_02)

    def test_user_fields(self) -> None:
        logger.info(">>> Starting USER fields test...")
        self.assertEqual(self.user_01.fullname, "Administrador", "Should be 'Administrador'...")
        self.assertEqual(self.user_01.email, "admin.24@gmail.com", "Should be 'admin.24@gmail.com'...")
        self.assertTrue(self.user_01.hashed_password == self.hashed_password,
                        f"Should be '{self.hashed_password}'...")
        self.assertEqual(self.user_01.role, UserRole.ADMIN, "Should be 'UserRole.ADMIN'...")

        self.assertEqual(self.user_02.fullname, "Cliente", "Should be 'Cliente'...")
        self.assertEqual(self.user_02.email, "client.24@gmail.com", "Should be 'client.24@gmail.com'...")
        self.assertFalse(self.user_02.hashed_password == "client1234",
                         f"Should be '{sha256('client1234'.encode()).hexdigest()}'...")
        self.assertEqual(self.user_02.role, UserRole.CLIENT, "Should be 'UserRole.CLIENT'...")
