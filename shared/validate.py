import re

from shared.logger_setup import main_logger as logger
from shared.utils.masker import mask_number


class Validate:
    """
    This class helps to validate any element with different methods using regular expressions.
    Other formulas can be implemented in the future.
    """
    @staticmethod
    def is_valid_email(email: str) -> bool:
        """
        Email must have local-part and domain separated by an @ sign.
        :param email: email user input
        :return: boolean
        """
        # This pattern allows to validate an email
        sequence = r"^([\w]+\.?)+@+[\w]+\.+[\w]{2,3}$"
        return True if re.match(sequence, email) else False

    @staticmethod
    def is_valid_password(password: str) -> bool:
        """
        Password must have at least one uppercase, one lowercase and one number.
        :param password: password user input
        :return: boolean
        """
        # This pattern allows to validate a password
        sequence = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$"
        return True if re.match(sequence, password) else False

    @staticmethod
    def is_valid_address(site_address: str) -> bool:
        """
        Site addres must have scheme, subdomain, domain and top-level domain.
        The subdirectory is not necessary.
        :param site_address: address user input
        :return: boolean
        """
        # This pattern allows to validate a password
        sequence = (r"((http)?s?:?(\/\/)?(www)?\.?)[a-zA-Z0-9-]+\.[a-z]{2,3}\/?([a-zA-Z0-9\~\@\#\$\%\^\&\*\("
                   r"\)_\-\=\+\\\/\?\.\:\;\'\,]*)?")
        return True if re.match(sequence, site_address) else False

    @staticmethod
    def is_valid_creditcard_number(creditcard_number: str) -> bool:
        """
        Creditcard number must be tested by The Luhn Formula.
        :param creditcard_number: creditcard number input
        :return: boolean
        """
        if len(creditcard_number) < 16 or len(creditcard_number) > 19:
            return False

        try:
            # Cast text to number
            list_numbers = [int(number) for number in creditcard_number]

        except ValueError as error_message:
            logger.error(f"Datos introducidos '{mask_number(creditcard_number)}': {error_message}")
            return False

        else:
            # Drop control digit
            control_digit = list_numbers.pop(-1)

            # Reverse list
            list_numbers.reverse()

            # Duplicate odd index number
            list_numbers = [number * 2 if index % 2 == 0 else number for index, number in enumerate(list_numbers)]

            # Substract 9 to numbers over 9:
            list_numbers = [number - 9 if number > 9 else number for number in list_numbers]

            # Add control digit again
            list_numbers.append(control_digit)

            # Add numbers
            total = sum(list_numbers)
            return total % 10 == 0

    @staticmethod
    def is_valid_date(new_date: str) -> bool:
        """
        Date must have the next format: 'mm/yy'.
        :param new_date: date user input
        :return: boolean
        """
        # This pattern allows to validate a date
        sequence = r"^(0[1-9]|1[0-2])\/([0-9][0-9])$"
        return True if re.match(sequence, new_date) else False

    def __str__(self) -> str:
        return f"<class Validate({dir(self)})>"
