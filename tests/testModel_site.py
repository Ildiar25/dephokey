import unittest
from types import NoneType

from features.encryption.core import decrypt_data
from features.models.user import User, UserRole
from features.models.site import Site

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


class SiteBuilder:
    def __init__(self) -> None:
        """Helps to create Site instance."""
        self.__site = Site(address="www.address.com", name=None, username="PepitoContento25",
                           password="User_1234", user=UserBuilder().build())

    def with_name(self, new_name: str) -> "SiteBuilder":
        self.__site.name = new_name
        return self

    def build(self) -> Site:
        return self.__site


class TestSite(unittest.TestCase):
    def setUp(self) -> None:
        logger.info("Preparing SITE instance...")

        # Create new instance
        self.site = SiteBuilder().build()
        self.password = "User_1234"

        logger.info("SITE instance ready for test...")

    def tearDown(self) -> None:
        del self.site

    def test_siteExists(self) -> None:
        self.log_instance(self.site)
        self.assertIsNotNone(self.site, msg="SITE instance doesn't exist.")
        logger.info(">>> Confirm if SITE exists...   OK")

    def test_siteType(self) -> None:
        self.assertIsInstance(self.site, Site, msg="Site MUST BE site type.")
        logger.info(">>> Confirm if SITE is instance of SITE...   OK")

    def test_siteUserExists(self) -> None:
        self.assertIsNotNone(self.site.user, msg="Site MUST HAVE an user.")
        logger.info(">>> Confirm if SITE has USER...   OK")

    def test_siteUserType(self) -> None:
        self.assertIsInstance(self.site.user, User, msg="Site user MUST BE user type.")
        logger.info(">>> Confirm if SITE USER is instance of USER...   OK")

    def test_siteAddressExists(self) -> None:
        self.assertIsNotNone(self.site.address, msg="Site MUST HAVE an address.")
        logger.info(">>> Confirm if SITE has ADDRESS...   OK")

    def test_siteAddressType(self) -> None:
        self.assertIsInstance(self.site.address, str, msg="Site address MUST BE string type.")
        logger.info(">>> Confirm if SITE ADDRESS is instance of STRING...   OK")

    def test_siteNameType(self) -> None:
        if self.site.name is not None:
            self.assertIsInstance(self.site.name, str, msg="Site name MUST BE none | string type.")
            logger.info(">>> Confirm if SITE NAME is instance of STRING...   OK")
            return
        self.assertIsInstance(self.site.name, NoneType, msg="Site name MUST BE none | string type")
        logger.info(f">>> Confirm if SITE NAME is instance of NONE...   OK")

    def test_siteUsernameExists(self) -> None:
        self.assertIsNotNone(self.site.username, msg="Site MUST HAVE an username.")
        logger.info(">>> Confirm if SITE has USERNAME...   OK")

    def test_siteUsernameType(self) -> None:
        self.assertIsInstance(self.site.username, str, msg="Site username MUST BE string type.")
        logger.info(">>> Confirm if SITE NAME is instance of STRING...   OK")

    def test_sitePasswordExists(self) -> None:
        self.assertIsNotNone(self.site.encrypted_password, msg="Site MUST HAVE a password.")
        logger.info(">>> Confirm if SITE has PASSWORD...   OK")

    def test_sitePasswordType(self) -> None:
        self.assertIsInstance(self.site.encrypted_password, str, msg="Site password MUST BE string type.")
        logger.info(">>> Confirm if SITE PASSWORD is instance of STRING...   OK")

    def test_sitePasswordEncrypted(self) -> None:
        self.assertEqual(self.password, decrypt_data(self.site.encrypted_password), msg="Site password MUST BE equal.")
        logger.info(">>> Confirm if SITE PASSWORD is ENCRYPTED...   OK")

    @staticmethod
    def log_instance(site: Site) -> None:
        logger.debug(site)


if __name__ == "__main__":
    unittest.main()
