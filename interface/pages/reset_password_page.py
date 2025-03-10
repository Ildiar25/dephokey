from datetime import timedelta

import flet as ft
import datetime
import asyncio

from data.db_orm import session

from features.models.user import User
from features.models import PasswordRequest
from features.email_management.send_email import SendEmail
from features.data_encryption.core import decrypt_data

from interface.pages.forms.base_form import FormStyle
from interface.pages.forms import ChangePasswordForm
from interface.controls import *

from shared.logger_setup import main_log as log
from shared.utils.colors import *
from shared.validate import Validate
from shared.generators import GenerateToken


class CountDown(ft.Text):
    def __init__(self, seconds: int, page: ft.Page):
        super().__init__()

        self.page = page
        self.seconds = seconds
        self.running = False
        self.size = 220
        self.color = accentTextColor
        self.font_family = "AlbertSansB"

    def start(self) -> None:
        self.running = True
        self.page.run_task(self.__update_timer)

    def stop(self) -> None:
        self.running = False

    async def __update_timer(self):
        while self.seconds and self.running:
            mins, secs = divmod(self.seconds, 60)
            self.value = "{:02d}:{:02d}".format(mins, secs)
            self.update()
            await asyncio.sleep(1)
            self.seconds -= 1
        self.value = "00:00"
        self.update()
        await asyncio.sleep(3)
        self.page.go("/login")


class ResetPasswordPage(ft.Container):
    def __init__(self, page: ft.Page) -> None:
        super().__init__()

        # General attributes
        self.page = page
        self.snackbar = Snackbar()
        self.user : User | None = None

        # ResetPassword attributes
        self.main_field = CustomTextField(label="Correo Electrónico", on_change=None)
        self.submit_email = CustomElevatedButton(
            name="¡Enviar!", style=ButtonStyle.DEFAULT, on_click=self.__send_email, height=45
        )
        self.expires_at: datetime.datetime | None = None
        self.countdown = CountDown(seconds=300, page=self.page)

        # Page design
        self.expand = True
        self.bgcolor = bgGeneralFormColor
        self.padding = ft.padding.symmetric(vertical=56, horizontal=32)

        # Invisible content
        self.validate = CustomElevatedButton(
            name="Validar", style=ButtonStyle.DEFAULT, width=220, disabled=True, on_click=self.__verify_token
        )
        self.char_01 = CustomTextField(max_length=1, width=50, on_change=self.toggle_login_button_state,
                                       text_align="center")
        self.char_02 = CustomTextField(max_length=1, width=50, on_change=self.toggle_login_button_state,
                                       text_align="center")
        self.char_03 = CustomTextField(max_length=1, width=50, on_change=self.toggle_login_button_state,
                                       text_align="center")
        self.char_04 = CustomTextField(max_length=1, width=50, on_change=self.toggle_login_button_state,
                                       text_align="center")
        self.char_05 = CustomTextField(max_length=1, width=50, on_change=self.toggle_login_button_state,
                                       text_align="center")
        self.char_06 = CustomTextField(max_length=1, width=50, on_change=self.toggle_login_button_state,
                                       text_align="center")
        self.char_07 = CustomTextField(max_length=1, width=50, on_change=self.toggle_login_button_state,
                                       text_align="center")

        self.change_content = ft.Container(
            visible=False,
            padding=ft.padding.only(top=40),
            expand=True,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Column(
                        width=800,
                        spacing=40,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            self.countdown,
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    self.char_01,
                                    self.char_02,
                                    self.char_03,
                                    self.char_04,
                                    self.char_05,
                                    self.char_06,
                                    self.char_07,
                                ]
                            ),
                            self.validate
                        ]
                    )
                ]
            )
        )

        # Body content
        self.content = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.IconButton(
                            ft.Icons.KEYBOARD_DOUBLE_ARROW_LEFT_ROUNDED,
                            icon_color=primaryCorporateColor,
                            on_click=self.__go_back,
                            highlight_color=neutral20,
                            hover_color=neutral10
                        )
                    ]
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        self.main_field, self.submit_email, self.snackbar
                    ]
                ),
                self.change_content
            ]
        )

        log.info("Página 'RESET PASSWORD' creada.")

    def toggle_login_button_state(self, _: ft.ControlEvent) -> None:
        if all((
            self.char_01.value,
            self.char_02.value,
            self.char_03.value,
            self.char_04.value,
            self.char_05.value,
            self.char_06.value,
            self.char_07.value,
        )):
            self.validate.disabled = False
        else:
            self.validate.disabled = True
        self.validate.update()

    def __go_back(self, _: ft.ControlEvent) -> None:
        self.change_content.visible = False
        self.change_content.update()
        self.countdown.stop()
        self.page.go("/login")

    def __send_email(self, _: ft.ControlEvent) -> None:
        email = self.main_field.value.strip().lower()
        self.user = session.query(User).filter_by(email=email).first()

        if not Validate.is_valid_email(email):
            self.snackbar.change_style(msg=f"'{email}' no es un email válido.", style=SnackbarStyle.DANGER)
            self.snackbar.update()
            return

        if not self.user:
            self.snackbar.change_style(msg=f"El usuario '{email}' no existe.", style=SnackbarStyle.DANGER)
            self.snackbar.update()
            return

        self.expires_at = datetime.datetime.now() + timedelta(minutes=5)
        self.snackbar.change_style(
            msg=f"De acuerdo, {self.user.fullname}. Se te ha enviado un correo con 7 caracteres.\n¡Tienes 5 minutos "
                f"para introducirlos en los campos que han aparecido!",
            style=SnackbarStyle.SUCCESS)
        self.snackbar.update()

        # Save new password request
        token = GenerateToken.tokenize()
        password_request = PasswordRequest(code=token, user=self.user)
        session.add(password_request)
        session.commit()

        # Reset form
        self.main_field.value = ""
        self.main_field.update()
        self.submit_email.disabled = True
        self.submit_email.update()

        # Show content
        self.change_content.visible = True
        self.change_content.update()
        self.countdown.start()

        # Send email
        new_email = SendEmail(token=token, user=self.user)
        new_email.send()

    def __verify_token(self, _: ft.ControlEvent) -> None:
        new_request = session.query(PasswordRequest).order_by(PasswordRequest.created.desc()).filter_by(
            user_id=self.user.id).first()
        code = "".join([
            self.char_01.value.strip().upper(),
            self.char_02.value.strip().upper(),
            self.char_03.value.strip().upper(),
            self.char_04.value.strip().upper(),
            self.char_05.value.strip().upper(),
            self.char_06.value.strip().upper(),
            self.char_07.value.strip().upper(),
        ])

        if self.expires_at < datetime.datetime.now():
            self.snackbar.change_style(
                msg="Lo siento, el tiempo ha expirado.\nVuelve a intentarlo de nuevo.", style=SnackbarStyle.INFO)
            self.snackbar.update()
            return

        if not decrypt_data(new_request.encrypted_code) == code:
            self.snackbar.change_style(
                msg="El token no es válido.", style=SnackbarStyle.DANGER)
            self.snackbar.update()
            return

        self.countdown.stop()
        self.change_content.visible = False
        self.change_content.update()

        self.page.open(
            ChangePasswordForm(self.page, self.snackbar, FormStyle.RESET, self.user.email)
        )

        self.submit_email.disabled = False
        self.submit_email.update()
