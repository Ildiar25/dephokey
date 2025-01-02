import flet as ft
import time
from hashlib import sha256

from data.db_orm import session

from features.models.user import User

from interface.controls import *

from shared.validate import Validate
from shared.logger_setup import main_logger as logger
from shared.utils.colors import *


class Login(ft.Container):
    def __init__(self, page: ft.Page) -> None:
        super().__init__()

        # General attributes
        self.page = page
        self.snackbar = ft.SnackBar(
            bgcolor=bgSnackBarDanger,
            content=ft.Text(
                "",
                text_align=ft.TextAlign.CENTER,
                color=mainDangerTextColor
            )
        )

        # Page design
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.update()

        # Login attributes
        self.email = CustomTextField(
            label="Correo electrónico",
            autofocus=True,
            on_change=self.enable_button
        )
        self.password = CustomTextField(
            label="Contraseña",
            can_reveal_password=True,
            password=True,
            on_change=self.enable_button
        )
        self.login_button = CustomElevatedButton(
            "LOGIN",
            width=300,
            disabled=True,
            on_click=self.login_function
        )
        self.forgot_password = ft.Container(
            on_hover=self.focus_link,
            on_click=self.forgot_password,
            content=ft.Text(
                "Olvidé la contraseña",
                color=mainSecondaryTextColor
            )
        )

        # Main container settings
        self.width = 800
        self.height = 500
        self.border_radius = 15
        self.shadow = ft.BoxShadow(2, blur_radius=8, color=shadowLogForm)

        # Login elements
        self.content = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=0,
            controls=[
                ft.Container(
                    width=400,
                    height=500,
                    alignment=ft.alignment.center,
                    bgcolor=lightColorBackground,
                    content=ft.Column(
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Container(
                                width=300,
                                height=250,
                                bgcolor=lightColorBackground,
                                content=ft.Column(
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    controls=[
                                        ft.Text("¡Bienvenido a Dephokey!", size=24),
                                        self.email,
                                        self.password,
                                        self.login_button,
                                        ft.Row(
                                            controls=[
                                                self.forgot_password
                                            ]
                                        ),
                                        ft.Divider(color=accentElementForm, thickness=2)
                                    ]
                                )
                            ),
                            ft.Text("¿Aún no tienes una cuenta?"),
                            CustomTextButton("Crea una cuenta", on_click=lambda _: self.page.go("/signup")),
                            self.snackbar
                        ]
                    )
                ),
                ft.Container(
                    width=400,
                    height=500,
                    alignment=ft.alignment.center,
                    bgcolor=bgAccentForm,
                    image=ft.DecorationImage("interface/assets/bg-image-01.png", fit=ft.ImageFit.COVER),
                    content=ft.Icon(ft.Icons.LOCK, size=150, color=accentElementForm)
                )
            ]
        )

    def enable_button(self, _: ft.ControlEvent) -> None:
        if self.email.value and self.password.value:
            self.login_button.disabled = False
        else:
            self.login_button.disabled = True

        self.login_button.update()

    def focus_link(self, action: ft.ControlEvent):
        if action and self.forgot_password.content.color == mainSecondaryTextColor:
            self.forgot_password.content.color = accentElementForm
        else:
            self.forgot_password.content.color = mainSecondaryTextColor

        self.forgot_password.update()

    def forgot_password(self, _: ft.ControlEvent):
        try:
            raise NotImplementedError("Implementar lógica nueva contraseña vía email")

        except NotImplementedError as error_message:
            logger.error(f"Llamada a la función '{Login.forgot_password.__name__}': {error_message}")

    def login_function(self, _: ft.ControlEvent) -> None:

        email_input: str = self.email.value.strip().lower()
        password_input: str = self.password.value.strip()

        # First, validate email and password
        if not (Validate.is_valid_email(email_input) and Validate.is_valid_password(password_input)):
            self.snackbar.content.value = ("El correo electrónico o la contraseña no son válidos.\n"
                                           "La contraseña debe tener al menos un número, una minúscula y "
                                           "una mayúscula.")
            self.snackbar.open = True
            self.snackbar.update()

        else:
            # Second, check if email already exists
            if not session.query(User).filter(User.email == email_input).first():
                self.snackbar.content.value = "¡El usuario no existe!"
                self.snackbar.open = True
                self.snackbar.update()

            else:
                # Third, load user and hashed input password
                user: User = session.query(User).filter(User.email == email_input).first()
                hashed_password = sha256(password_input.encode()).hexdigest()

                # Compare data inputs with loaded data
                if not all((user.email == email_input, user.hashed_password == hashed_password)):
                    self.snackbar.content.value = "El correo electrónico o la contraseña no son válidos."
                    self.snackbar.open = True
                    self.snackbar.update()

                else:
                    # Create new session
                    self.page.session.set("session", user)

                    # Report page loading
                    self.page.overlay.append(
                        ft.Container(
                            alignment=ft.alignment.center,
                            expand=True,
                            bgcolor=ft.Colors.with_opacity(0.3, lightColorBackground),
                            content=ft.ProgressRing(
                                color=accentGeneralElementColor
                            )
                        )
                    )
                    self.page.update()

                    # Load login page
                    time.sleep(2)
                    self.page.overlay.clear()
                    self.page.go("/home")
