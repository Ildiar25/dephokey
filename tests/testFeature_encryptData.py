import unittest

from features.data_encryption.core import decrypt_data, encrypt_data
from shared.logger_setup import test_log as log

# TODO: Implement data-encrypt module tests

class TestEncrypData(unittest.TestCase):
    def setUp(self) -> None:
        log.info("Preparing DATA ENCRYPTION module...")

        # Create comparable elements
        self.name = ""


    def tearDown(self) -> None:
        pass
