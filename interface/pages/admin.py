import flet as ft

from interface.controls import *

from shared.utils.colors import *


class Admin(ft.Container):
    def __init__(self, page: ft.Page) -> None:
        super().__init__()

        # General attributes
        self.page = page

        # Main container settings
        self.expand = True
        self.gradient = ft.LinearGradient(
            bgGradientAdminColor,
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center
        )

        # Admin elements
        self.content = ft.Row(
            controls=[
                ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.AUTO,
                    controls=[
                        ft.Text(
                            "Añadir Usuario:"
                        ),
                        ft.Row(
                            expand=True,
                            controls=[
                                CustomTextField(
                                    label="Nombre Completo",
                                    autofocus=True
                                ),
                                CustomTextField(
                                    label="Usuario"
                                ),
                                CustomTextField(
                                    label="Contraseña",
                                    password=True,
                                    can_reveal_password=True
                                ),
                                CustomButton(
                                    "AÑADIR",
                                    width=200
                                )
                            ]
                        )
                    ]
                )
            ]
        )

