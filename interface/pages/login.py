import flet as ft
import time

from data.db_orm import session

# from features.models.user import User

from interface.controls import *

from shared.validate import Validate
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
            "Correo electrónico",
            autofocus=True
        )
        self.password = CustomTextField(
            "Contraseña",
            can_reveal_password=True,
            password=True
        )
        self.login_button = CustomElevatedButton(
            "LOGIN",
            width=300,
            disabled=True,
            on_click=self.login_function
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
                                        self.login_button
                                    ]
                                )
                            ),
                            ft.Text("¿Aún no tienes una cuenta?"),
                            CustomTextButton("Crea una cuenta")
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

    def login_function(self, _: ft.ControlEvent) -> None:
        pass
