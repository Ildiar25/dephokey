from pathlib import Path
from jinja2.exceptions import TemplateNotFound
from jinja2 import Environment, FileSystemLoader

from features.models.user import User  # Circular import error with SQLAlchemy and Literal if executes from here
from features.encryption.core import decrypt_data

from shared.logger_setup import main_logger as logger


class Email:

    def __init__(self, user: User, encrypt_code: str) -> None:
        self.name = user.fullname.split(" ")[0]
        self.receiver = user.email
        self.code = decrypt_data(encrypt_code)
        self.message_content = self.create(self.name, self.code)

    @staticmethod
    def create(name: str, code: str) -> tuple[str, str] | str:

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

        except TemplateNotFound as not_template:
            logger.error(f"{type(not_template).__name__} ::: No se ha encontrado la plantilla HTML.")
            return plain_text_email
        # Return new HTML
        else:
            return html_doc, plain_text_email

    def send(self) -> None:
        pass
