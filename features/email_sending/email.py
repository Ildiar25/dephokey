from pathlib import Path
from jinja2.exceptions import TemplateNotFound
from jinja2 import Environment, FileSystemLoader

from features.models.user import User  # Circular import error with SQLAlchemy and Literal if executes from here
from features.encryption.core import decrypt_data

from shared.logger_setup import main_logger as logger


class Email:

    def __init__(self, user: User, encrypt_code: str) -> None:
        self.name: str = user.fullname.split(" ")[0]
        self.receiver: str = user.email
        self.code: str = " ".join([ch for ch in decrypt_data(encrypt_code)])
        self.message_content: tuple[str, str | None] = self.__create(self.name, self.code)

    @staticmethod
    def __create(name: str, code: str) -> tuple[str, str | None]:

        plain_text_email = (f"Hola {name}!\nPor favor, introduce en el programa el código de siete caracteres "
                            f"proporcionado\npara poder actualizar tu contraseña:\n\n{code}\n\nSi no has realizado la "
                            f"petición, puedes ignorar este email.\n\nAtentamente,\nEl equipo Dephokey")

        # Loads file directory
        main_path = Path(__file__).parent
        env = Environment(loader=FileSystemLoader(f"{main_path}/templates"))

        # Loads template
        try:
            template = env.get_template("reset_password.html")
            html_doc = template.render(name=name, code=code)

        # Returns message content
        except TemplateNotFound as not_template:
            logger.error(f"{type(not_template).__name__} ::: No se ha encontrado la plantilla HTML.")
            return plain_text_email, None
        else:
            return plain_text_email, html_doc

    def send(self) -> None:
        # Prepares connection with server

        # Prepares message content

        # Send message and report
        pass
