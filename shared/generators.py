from string import ascii_lowercase, digits, ascii_uppercase
import random
import nanoid


class GenerateID:
    """
    This class allows to generate diferents ID's according to need.
    """
    @staticmethod
    def short_id() -> str:
        return nanoid.generate(ascii_lowercase + digits, 15)


class GenerateToken:
    """
    This class allows to generate a random token according to need.
    """
    @staticmethod
    def tokenize(size: int = 7) -> str:
        return "".join(random.choices(ascii_uppercase + digits, k=size))
