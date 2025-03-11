import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from features.models.user import User
from .create_message import CreateMessage

from shared.utils.masker import mask_number, mask_email
from shared.logger_setup import main_log as log


class SendEmail:
    def __init__(self, user: User, token: str) -> None:
        # Server config
        self.smtp_host = "localhost"
        self.smtp_port = 1025

        # User data
        self.name = user.fullname.split(" ")[0]
        self.recipient = user.email

        # Sender data
        self.sender = "dephokey.team@gmail.com"

        # Message
        self.body = CreateMessage(self.name, token)

    def send(self) -> bool:
        # New Message
        msg = MIMEMultipart()
        msg["From"] = self.sender
        msg["To"] = self.recipient
        msg["Subject"] = "Tu token para Dephokey está listo"

        # Image attachment
        try:
            with open("features/email_management/templates/assets/logotype.png", "rb") as image:
                img = MIMEBase("logotype", "png")
                img.set_payload(image.read())
                encoders.encode_base64(img)
                img.add_header("Content-ID", "<logotype.png>")
                img.add_header("Content-Disposition", "inline", filename="logotype.png")
                msg.attach(img)

        except FileNotFoundError as not_found:
            log.error(f"{type(not_found).__name__} | No se ha encontrado el logotipo para el email: {not_found}.")
        except PermissionError as not_allowed:
            log.error(f"{type(not_allowed).__name__} | No se tienen permisos para leer el archivo: {not_allowed}.")

        msg.attach(MIMEText(self.body.with_text, "plain"))
        msg.attach(MIMEText(self.body.with_html, "html"))

        try:
            smtp = smtplib.SMTP(self.smtp_host, self.smtp_port)
            smtp.send_message(msg)
            smtp.quit()
            return True

        except ConnectionRefusedError as not_allowed:
            log.error(f"{type(not_allowed).__name__} | Se ha denegado la conexión: {not_allowed}.")
            return False
        except ConnectionError as not_connected:
            log.error(f"{type(not_connected).__name__} | No se ha podido establecer la conexión: {not_connected}.")
            return False
        except Exception as unknown:
            log.error(f"{type(unknown).__name__} | Un error inesperado ha ocurrido al tratar de enviar el correo: "
                      f"{unknown}.")
            return False

    def __str__(self) -> str:
        return (f"<class SendEmail(smtp_host={repr(mask_number(self.smtp_host))}, "
                f"smtp_port={repr(mask_number(str(self.smtp_port)))}, sender={repr(mask_email(self.sender))}, "
                f"recipient={repr(mask_email(self.recipient))}, body={self.body})>")
