import asyncio
import datetime

import flet as ft

from data.db_orm import session
from features.data_encryption.core import decrypt_data
from features.email_management.create_message import MessageStyle
from features.email_management.send_email import SendEmail
from features.models import PasswordRequest
from features.models.user import User
from interface.controls import CustomElevatedButton, CustomTextField
from interface.controls.e_button import ButtonStyle
from interface.controls.snackbar import Snackbar, SnackbarStyle
from interface.pages.forms import ChangePasswordForm
from interface.pages.forms.base_form import FormStyle
from shared.logger_setup import main_log as log
from shared.utils.colors import accentTextColor, neutral00, neutral10, neutral20, primaryCorporateColor
from shared.validate import Validate


SECONDS_AWAIT = 300


class CountDown(ft.Text):
    """
    This class helps to display a text-based control countdown for UX.
    It is possible to change showed time adding just seconds.
    """

    def __init__(self, seconds: int, page: ft.Page):
        super().__init__()

        # Countdown settings
        self.page = page
        self.seconds = seconds
        self.running = False

        # Design settings
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
            self.value = f"{mins:02d}:{secs:02d}"
            self.update()

            await asyncio.sleep(1)
            self.seconds -= 1

        self.value = "00:00"
        self.update()


class ResetPasswordPage(ft.Container):
    """Creates ResetPassword page and displays all form elements"""
    def __init__(self, page: ft.Page) -> None:
        super().__init__()

        # Page attributes
        self.page = page
        self.snackbar = Snackbar()
        self.user: User | None = None

        # ResetPassword attributes
        self.main_field = CustomTextField(label="Correo Electrónico", on_change=None, on_submit=self.__submit_email)
        self.submit_email = CustomElevatedButton(
            name="¡Enviar!",
            style=ButtonStyle.DEFAULT,
            on_click=self.__submit_email,
            height=45
        )
        self.countdown = CountDown(seconds=SECONDS_AWAIT, page=self.page)

        # Page design
        self.expand = True
        self.bgcolor = neutral00
        self.padding = ft.padding.symmetric(vertical=56, horizontal=32)

        # Invisible content
        self.validate = CustomElevatedButton(
            name="Validar",
            style=ButtonStyle.DEFAULT,
            width=220,
            disabled=True,
            on_click=self.__verify_token
        )
        self.char_01 = CustomTextField(
            max_length=1,
            width=50,
            on_change=self.__toggle_login_button_state,
            text_align="center"
        )
        self.char_02 = CustomTextField(
            max_length=1,
            width=50,
            on_change=self.__toggle_login_button_state,
            text_align="center"
        )
        self.char_03 = CustomTextField(
            max_length=1,
            width=50,
            on_change=self.__toggle_login_button_state,
            text_align="center"
        )
        self.char_04 = CustomTextField(
            max_length=1,
            width=50,
            on_change=self.__toggle_login_button_state,
            text_align="center"
        )
        self.char_05 = CustomTextField(
            max_length=1,
            width=50,
            on_change=self.__toggle_login_button_state,
            text_align="center"
        )
        self.char_06 = CustomTextField(
            max_length=1,
            width=50,
            on_change=self.__toggle_login_button_state,
            text_align="center"
        )
        self.char_07 = CustomTextField(
            max_length=1,
            width=50,
            on_change=self.__toggle_login_button_state,
            on_submit=self.__verify_token,
            text_align="center"
        )

        self.hidden_content = ft.Container(
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
                            # Display countdown text
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
                            self.validate,
                        ]
                    ),
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
                            on_click=self.__nav_to_login,
                            highlight_color=neutral20,
                            hover_color=neutral10,
                            focus_color=neutral10
                        )
                    ]
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[self.main_field, self.submit_email, self.snackbar, ]
                ),
                # Hidden content
                self.hidden_content,
            ]
        )

        log.info("Página 'PW_RECOVER GENERATE_PW' creada.")

    def __toggle_login_button_state(self, _: ft.ControlEvent) -> None:
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

    def __nav_to_login(self, _: ft.ControlEvent) -> None:
        self.__hide_content()
        self.page.go("/login")

    def __submit_email(self, _: ft.ControlEvent) -> None:
        email = self.main_field.value.strip().lower()
        self.user = session.query(User).filter_by(email=email).first()

        if not Validate.is_valid_email(email):
            self.__display_message(msg=f"'{email}' no es un email válido.", style=SnackbarStyle.DANGER)
            return

        if not self.user:
            self.__display_message(msg=f"El usuario '{email}' no existe.", style=SnackbarStyle.DANGER)
            return

        # Create & save a PasswordRequest instance
        pw_request = self.__create_password_instance()
        self.__send_email(pw_request)

    def __create_password_instance(self) -> PasswordRequest:
        pw_request = PasswordRequest(user=self.user)
        session.add(pw_request)
        session.commit()

        return pw_request

    def __send_email(self, pw_request: PasswordRequest) -> None:
        new_email = SendEmail(
            msg_style=MessageStyle.RESET,
            send_to=self.user.email,
            name=self.user.fullname.split(" ")[0],
            token=decrypt_data(pw_request.encrypted_code)
        )

        if not new_email.send():
            self.__display_message(
                msg="Ha habido un problema durante el envío del mensaje.\nContacta con el Soporte Técnico",
                style=SnackbarStyle.DANGER
            )
            self.__hide_content()
            return

        self.__show_content()
        self.__display_message(
            msg=f"De acuerdo, {self.user.fullname}. Se te ha enviado un correo con 7 caracteres.\n¡Tienes 5 minutos "
                f"para introducirlos en los campos que han aparecido!",
            style=SnackbarStyle.SUCCESS
        )

    def __verify_token(self, _: ft.ControlEvent) -> None:
        # noinspection PyPep8Naming
        PR: type[PasswordRequest] = PasswordRequest
        new_pw_request = session.query(PR).order_by(PR.created.desc()).filter_by(user_id=self.user.id).first()
        code = self.__get_token()

        if datetime.datetime.now() > new_pw_request.expires_at:
            self.__display_message(
                msg="Lo siento, el tiempo ha expirado.\nVuelve a intentarlo de nuevo.", style=SnackbarStyle.INFO
            )
            return

        if decrypt_data(new_pw_request.encrypted_code) != code:
            self.__display_message(msg="El token no es válido.", style=SnackbarStyle.DANGER)
            return

        self.__reset_page()

        # Open change password form
        self.page.open(
            ChangePasswordForm(self.page, self.snackbar, FormStyle.PW_RECOVER, self.user.email)
        )

    def __get_token(self) -> str:
        return "".join([
            self.char_01.value.strip().upper(),
            self.char_02.value.strip().upper(),
            self.char_03.value.strip().upper(),
            self.char_04.value.strip().upper(),
            self.char_05.value.strip().upper(),
            self.char_06.value.strip().upper(),
            self.char_07.value.strip().upper(),
        ])

    def __reset_page(self) -> None:
        self.countdown.stop()
        self.countdown.seconds = SECONDS_AWAIT
        self.char_01.value = ""
        self.char_02.value = ""
        self.char_03.value = ""
        self.char_04.value = ""
        self.char_05.value = ""
        self.char_06.value = ""
        self.char_07.value = ""
        self.__hide_content()

    def __show_content(self) -> None:
        self.main_field.value = ""
        self.submit_email.disabled = True
        self.countdown.start()
        self.hidden_content.visible = True
        self.content.update()

    def __hide_content(self) -> None:
        self.main_field.value = ""
        self.submit_email.disabled = False
        self.hidden_content.visible = False
        self.content.update()

    def __display_message(self, msg: str, style: SnackbarStyle) -> None:
        self.snackbar.change_style(msg=msg, style=style)
        self.snackbar.update()
