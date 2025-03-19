import smtplib

from shared.logger_setup import main_log as log

from .create_message import CreateMessage, MessageStyle


class SendEmail:
    def __init__(self, msg_style: MessageStyle, **kwargs) -> None:
        # Server config
        self.smtp_host = "localhost"
        self.smtp_port = 1025

        self.message = CreateMessage(
            style=msg_style,
            **kwargs
        ).create()


    def send(self) -> bool:
        try:
            smtp = smtplib.SMTP(self.smtp_host, self.smtp_port)
            smtp.send_message(self.message)
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
        return (f"<class SendEmail(host={repr(self.smtp_host)}, port={repr(self.smtp_port)}, "
                f"message={repr(self.message)})>")
