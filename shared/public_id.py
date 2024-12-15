from string import ascii_lowercase, digits
import nanoid


class PublicID:
    """
    This class allows to generate diferents ID's according to need.
    """
    @staticmethod
    def generate_short_id() -> str:
        return nanoid.generate(ascii_lowercase + digits, 15)
