import flet as ft

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
                    controls=[
                        ft.Text("¡Hello World!")
                    ]
                )
            ]
        )

