import re

from shared.logger_setup import main_log as log
from shared.utils.masker import mask_number


class Validate:
    """
    This class helps to validate any element with different methods using regular expressions.
    Other formulas can be implemented in the future.
    """

    @staticmethod
    def is_valid_address(site_address: str) -> bool:
        """
        Site addres must have scheme, subdomain, domain and top-level domain.
        The subdirectory is not necessary.
        :param site_address: str | address user input
        :return: boolean | True if value is valid else False
        """

        protocol = r"((http)?s?:?(\/\/)?(www)?\.?)"
        domain_name = r"[a-zA-Z0-9-]+\."
        domain_extension = r"[a-z]{2,3}"
        path = r"\/?([a-zA-Z0-9\~\@\#\$\%\^\&\*\(\)_\-\=\+\\\/\?\.\:\;\'\,]*)?"

        # Creates pattern
        pattern = protocol + domain_name + domain_extension + path

        return bool(re.match(pattern, site_address))

    @staticmethod
    def is_valid_creditcard_number(creditcard_number: str) -> bool:
        """
        Creditcard number must be tested by The Luhn Formula.
        :param creditcard_number: str | creditcard number input
        :return: boolean | True if value is valid else False
        """
        if len(creditcard_number) < 16 or len(creditcard_number) > 19:
            return False

        try:
            # Cast text to number
            list_numbers = [int(number) for number in creditcard_number]

        except ValueError as error_message:
            log.error(f"{type(error_message).__name__} | "
                      f"No se han podido castear los datos a número entero: Datos introducidos "
                      f"{repr(mask_number(creditcard_number))} | {error_message}")
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
    def is_valid_email(email: str) -> bool:
        """
        Email must have local-part and domain separated by an @ sign.
        :param email: str | email user input
        :return: boolean | True if value is valid else False
        """

        local_name = r"^([\w]+\.?)+"
        domain = r"@+[\w]+\."
        extension = r"+[\w]{2,3}$"

        # Creates pattern
        pattern = local_name + domain + extension
        return bool(re.match(pattern, email))

    @staticmethod
    def is_valid_password(password: str) -> bool:
        """
        Password must have at least one uppercase, one lowercase and one number.
        :param password: str | password user input
        :return: boolean | True if value is valid else False
        """

        has_digit = r"^(?=.*\d)"
        has_lowercase = r"(?=.*[a-z])"
        has_uppercase = r"(?=.*[A-Z])"
        min_length = r".{8,}$"

        # Creates pattern
        pattern = has_digit + has_lowercase + has_uppercase + min_length
        return bool(re.match(pattern, password))

    @staticmethod
    def is_valid_date(new_date: str) -> bool:
        """
        Date must have the next format: 'mm/yy'.
        :param new_date: str | date user input
        :return: boolean | True if value is valid else False
        """

        month = r"^(0[1-9]|1[0-2])"
        sep = r"\/"
        year = r"([0-9][0-9])$"

        # Creates pattern
        pattern = month + sep + year
        return bool(re.match(pattern, new_date))

    def __str__(self) -> str:
        return (
            f"<class Validate("
                f"method={repr(self.is_valid_address.__name__)}, "
                f"method={repr(self.is_valid_creditcard_number.__name__)}, "
                f"method={repr(self.is_valid_email.__name__)}, "
                f"method={repr(self.is_valid_password.__name__)}, "
                f"method={repr(self.is_valid_date.__name__)}, "
            f")>"
        )
