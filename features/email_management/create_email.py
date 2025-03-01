from pathlib import Path
from jinja2.exceptions import TemplateNotFound
from jinja2 import Environment, FileSystemLoader

from features.models.user import User  # Circular import error with SQLAlchemy and Literal if executes from here

from shared.utils.masker import mask_text
from shared.logger_setup import main_log as log


class CreateEmail:

    def __init__(self, user: User, code: str) -> None:
        self.name: str = user.fullname.split(" ")[0]
        self.receiver: str = user.email
        self.code: str = code
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

            return plain_text_email, html_doc

        # Returns message content
        except TemplateNotFound as not_template:
            log.error(f"{type(not_template).__name__} ::: No se ha encontrado la plantilla HTML. {not_template}")
            return plain_text_email, None
        except Exception as unknown:
            log.error(f"{type(unknown).__name__} ::: Un error inesperado ha ocurrido al procesar la platilla "
                         f"HTML. {unknown}")
            return plain_text_email, None

    def __repr__(self) -> str:
        return (f"<class CreateEmail(name={repr(self.name)}, receiver={repr(self.receiver)}, "
                f"code={repr(mask_text(self.code))}, message={repr(mask_text(self.message_content[0]))})>")
