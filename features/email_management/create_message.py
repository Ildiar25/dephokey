from email.mime.text import MIMEText
from enum import Enum
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from jinja2.exceptions import TemplateNotFound
from jinja2 import Environment, FileSystemLoader

from shared.utils.masker import mask_text, mask_email
from shared.logger_setup import main_log as log


class MessageStyle(Enum):
    RESET = "reset"
    QUERY = "querty"


class CreateMessage(MIMEMultipart):
    def __init__(self, style: MessageStyle, send_from: str | None = None, send_to: str | None = None,
                 subject: str | None = None, token: str | None = None, name: str | None = None,
                 content: str | None = None) -> None:
        super().__init__()

        # General attributes
        self.path_img = Path(__file__).parent.joinpath("templates/assets/logotype.png")
        self["From"] = send_from if send_from else "dephokey.team@gmail.com"
        self["To"] = send_to if send_to else "dephokey.team@gmail.com"
        self["Subject"] = subject if subject else "¡Tu token para Dephokey está listo!"

        # Message attributes
        self.style = style
        self.name = name
        self.token = token
        self.img = self.__load_image()
        self.with_text = content
        self.with_html = None

        self.__update_appearance()

    def __update_appearance(self) -> None:
        match self.style:
            case MessageStyle.RESET:
                self.with_text = (f"Hola {self.name}!\nPor favor, introduce en el programa el código de siete "
                                  f"caracteres proporcionado\npara poder actualizar tu contraseña:\n\n{self.token}\n\n"
                                  f"Si no has realizado la petición, puedes ignorar este email.\n\nAtentamente,\n"
                                  f"El equipo Dephokey")
                self.with_html = self.__load_template(
                    template_name="reset_password.html", title=self.name, message=self.token
                )

            case MessageStyle.QUERY:
                self.with_html = self.__load_template(
                    template_name="user_request.html", title=self["subject"], message=self.with_text
                )

    def __load_image(self) -> MIMEBase | None:
        try:
            with open(self.path_img, "rb") as img:
                logo = MIMEBase("logotype", "png")
                logo.set_payload(img.read())
                encoders.encode_base64(logo)
                logo.add_header("Content-ID", "<logotype.png>")
                logo.add_header("Content-Disposition", "inline", filename="logotype.png")
                return logo

        except PermissionError as not_allowed:
            log.error(f"{type(not_allowed).__name__} | No se tienen permisos para leer el archivo: {not_allowed}.")
            return None
        except FileNotFoundError as not_found:
            log.error(f"{type(not_found).__name__} | No se ha encontrado el logotipo para el email: {not_found}.")
            return None

    @staticmethod
    def __load_template(template_name: str, title: str, message: str) -> str | None:
        # Loads file directory
        main_path = Path(__file__).parent
        env = Environment(loader=FileSystemLoader(f"{main_path}/templates"))

        try:
            new_template = env.get_template(template_name)
            return new_template.render(mail_title=title, mail_message=message)

        except TemplateNotFound as not_template:
            log.error(f"{type(not_template).__name__} | No se ha encontrado la plantilla HTML: {not_template}")
        except Exception as unknown:
            log.error(f"{type(unknown).__name__} | Un error inesperado ha ocurrido al procesar la platilla "
                      f"HTML: {unknown}")

    def create(self) -> "CreateMessage":
        if self.img:
            self.attach(self.img)
        if self.with_text:
            text_part = MIMEText(self.with_text, "plain")
            self.attach(text_part)
        if self.with_html:
            html_part = MIMEText(self.with_html, "html")
            self.attach(html_part)
        return self

    def __repr__(self) -> str:
        return (f"<class CreateEmail(from={repr(mask_email(self['From']))}, to={repr(mask_email(self['To']))}, "
                f"subject={repr(self['Subject'])}, content={repr(mask_text(self.with_text))})>")
