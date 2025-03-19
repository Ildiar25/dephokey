import random
from string import ascii_lowercase, ascii_uppercase, digits

import nanoid


class GenerateID:
    """
    This class allows to generate diferents ID's according to need.
    """

    @staticmethod
    def short_id() -> str:
        """
        Short ID generates a short ID with a given 15-character limit.
        :return: boolean | New ID
        """
        return nanoid.generate(alphabet=ascii_lowercase + digits, size=15)


class GenerateToken:
    """
    This class allows to generate a random token according to need with a given size.
    """

    @staticmethod
    def generate() -> str:
        """
        Generate create a token with a given 7-character limit.
        :return: str | New token
        """
        return "".join(random.choices(population=ascii_uppercase + digits, k=7))
