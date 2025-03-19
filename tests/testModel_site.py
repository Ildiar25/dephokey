import unittest
from types import NoneType

from features.data_encryption.core import decrypt_data
from features.models.site import Site
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


class SiteBuilder:
    def __init__(self) -> None:
        """Helps to create Site instance."""
        self.__site = Site(
            address="www.address.com",
            name=None,
            username="PepitoContento25",
            password="User_1234",
            user=UserBuilder().build()
        )

    def with_name(self, new_name: str) -> "SiteBuilder":
        self.__site.name = new_name
        return self

    def build(self) -> Site:
        return self.__site


class TestSite(unittest.TestCase):
    def setUp(self) -> None:
        log.info("Preparing SITE instance...")

        # Create new instance
        self.site = SiteBuilder().build()
        self.password = "User_1234"

        log.info("SITE instance ready for test...")

    def tearDown(self) -> None:
        del self.site

    def test_siteExists(self) -> None:
        self.log_instance(self.site)
        self.assertIsNotNone(
            obj=self.site,
            msg="SITE instance doesn't exist."
        )
        log.info(">>> Confirm if SITE exists...   OK")

    def test_siteType(self) -> None:
        self.assertIsInstance(
            obj=self.site,
            cls=Site,
            msg="Site MUST BE site type."
        )
        log.info(">>> Confirm if SITE is instance of SITE...   OK")

    def test_siteUserExists(self) -> None:
        self.assertIsNotNone(
            obj=self.site.user,
            msg="Site MUST HAVE an user."
        )
        log.info(">>> Confirm if SITE has USER...   OK")

    def test_siteUserType(self) -> None:
        self.assertIsInstance(
            obj=self.site.user,
            cls=User,
            msg="Site user MUST BE user type."
        )
        log.info(">>> Confirm if SITE USER is instance of USER...   OK")

    def test_siteAddressExists(self) -> None:
        self.assertIsNotNone(
            obj=self.site.address,
            msg="Site MUST HAVE an address."
        )
        log.info(">>> Confirm if SITE has ADDRESS...   OK")

    def test_siteAddressType(self) -> None:
        self.assertIsInstance(
            obj=self.site.address,
            cls=str,
            msg="Site address MUST BE string type."
        )
        log.info(">>> Confirm if SITE ADDRESS is instance of STRING...   OK")

    def test_siteNameType(self) -> None:
        if self.site.name is not None:
            self.assertIsInstance(
                obj=self.site.name,
                cls=str,
                msg="Site name MUST BE none | string type."
            )
            log.info(">>> Confirm if SITE NAME is instance of STRING...   OK")
            return

        self.assertIsInstance(
            obj=self.site.name,
            cls=NoneType,
            msg="Site name MUST BE none | string type"
        )
        log.info(">>> Confirm if SITE NAME is instance of NONE...   OK")

    def test_siteUsernameExists(self) -> None:
        self.assertIsNotNone(
            obj=self.site.username,
            msg="Site MUST HAVE an username."
        )
        log.info(">>> Confirm if SITE has USERNAME...   OK")

    def test_siteUsernameType(self) -> None:
        self.assertIsInstance(
            obj=self.site.username,
            cls=str,
            msg="Site username MUST BE string type."
        )
        log.info(">>> Confirm if SITE NAME is instance of STRING...   OK")

    def test_sitePasswordExists(self) -> None:
        self.assertIsNotNone(
            obj=self.site.encrypted_password,
            msg="Site MUST HAVE a password."
        )
        log.info(">>> Confirm if SITE has PASSWORD...   OK")

    def test_sitePasswordType(self) -> None:
        self.assertIsInstance(
            obj=self.site.encrypted_password,
            cls=str,
            msg="Site password MUST BE string type."
        )
        log.info(">>> Confirm if SITE PASSWORD is instance of STRING...   OK")

    def test_sitePasswordEncrypted(self) -> None:
        self.assertEqual(
            first=self.password,
            second=decrypt_data(self.site.encrypted_password),
            msg="Site password MUST BE equal."
        )
        log.info(">>> Confirm if SITE PASSWORD is ENCRYPTED...   OK")

    @staticmethod
    def log_instance(site: Site) -> None:
        log.debug(site)


if __name__ == "__main__":
    unittest.main()
