from pathlib import Path
from jinja2.exceptions import TemplateNotFound
from jinja2 import Environment, FileSystemLoader

from shared.utils.masker import mask_text
from shared.logger_setup import main_log as log


class CreateMessage:

    def __init__(self, name: str, token: str) -> None:
        self.name = name
        self.token: str = token
        self.with_text: str = self.__plain_text()
        self.with_html: str | None = self.__html_text()

    def __plain_text(self) -> str:
        return (f"Hola {self.name}!\nPor favor, introduce en el programa el código de siete caracteres "
                f"proporcionado\npara poder actualizar tu contraseña:\n\n{self.token}\n\nSi no has realizado la "
                f"petición, puedes ignorar este email.\n\nAtentamente,\nEl equipo Dephokey")

    def __html_text(self) -> str | None:
        # Loads file directory
        main_path = Path(__file__).parent
        env = Environment(loader=FileSystemLoader(f"{main_path}/templates"))

        # Loads template
        try:
            template = env.get_template("reset_password.html")
            html_doc = template.render(name=self.name, code=self.token)

            return html_doc

        except TemplateNotFound as not_template:
            log.error(f"{type(not_template).__name__} | No se ha encontrado la plantilla HTML: {not_template}")
        except Exception as unknown:
            log.error(f"{type(unknown).__name__} | Un error inesperado ha ocurrido al procesar la platilla "
                      f"HTML: {unknown}")

    def __repr__(self) -> str:
        return (f"<class CreateEmail(name={repr(self.name)}, code={repr(mask_text(self.token))}, "
                f"with_text={repr(mask_text(self.with_text))}, with_html={repr(mask_text(self.with_html))})>")
