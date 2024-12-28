import flet as ft
import time

from data.db_orm import session

from features.models.user import User

from interface.controls import *

from shared.validate import Validate
from shared.logger_setup import main_logger as logger
from shared.utils.colors import *


class Signup(ft.Container):
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

        # Signup attributes
        self.fullname = CustomTextField(
            "Nombre completo",
            text_size=14,
            on_change=self.enable_button
        )
        self.email = CustomTextField(
            "Correo electrónico",
            text_size=14,
            on_change=self.enable_button
        )
        self.password = CustomTextField(
            "Contraseña",
            text_size=14,
            password=True,
            on_change=self.enable_button
        )
        self.password_repeat = CustomTextField(
            "Contraseña",
            text_size=14,
            password=True,
            on_change=self.enable_button
        )
        self.signup_button = CustomElevatedButton(
            "SIGNUP",
            width=300,
            on_click=self.create_account,
            disabled=True
        )

        # Main container settings
        self.width = 800
        self.height = 500
        self.border_radius = 15
        self.shadow = ft.BoxShadow(2, blur_radius=8, color=shadowLogForm)

        # Signup elements
        self.content = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=0,
            controls=[
                ft.Container(
                    width=400,
                    height=500,
                    alignment=ft.alignment.center,
                    bgcolor=bgAccentForm,
                    image=ft.DecorationImage("interface/assets/bg-image-02.png", fit=ft.ImageFit.COVER),
                    content=ft.Icon(ft.Icons.VERIFIED_USER, size=150, color=accentElementForm)
                ),
                ft.Container(
                    width=400,
                    height=500,
                    bgcolor=lightColorBackground,
                    content=ft.Column(
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Container(
                                width=300,
                                height=350,
                                bgcolor=lightColorBackground,
                                content=ft.Column(
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    controls=[
                                        ft.Text("¡Bienvenido Usuario!", size=24),
                                        ft.Divider(color=accentElementForm, thickness=2),
                                        self.fullname,
                                        self.email,
                                        self.password,
                                        self.password_repeat,
                                        self.signup_button
                                    ]
                                )
                            ),
                            ft.Text("¿Ya tienes una cuenta?"),
                            CustomTextButton("Inicia sesión", on_click=lambda _: self.page.go("/login")),
                            self.snackbar
                        ]
                    )
                )
            ]
        )

    def enable_button(self, _: ft.ControlEvent) -> None:
        if all((self.fullname.value, self.email.value, self.password.value, self.password_repeat.value)):
            self.signup_button.disabled = False
        else:
            self.signup_button.disabled = True

        self.signup_button.update()

    def create_account(self, _: ft.ControlEvent) -> None:
        try:
            raise NotImplementedError("Implementar lógica de creación de cuenta")

        except NotImplementedError as error_message:
            logger.error(f"Llamada a la función '{Signup.create_account.__name__}': {error_message}")
