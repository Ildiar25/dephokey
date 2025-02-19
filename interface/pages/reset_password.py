import flet as ft

from interface.controls import CustomTextField, CustomElevatedButton
from shared.utils.colors import *


class ResetPasswordPage(ft.Container):
    def __init__(self, page: ft.Page) -> None:
        super().__init__()

        # General attributes
        self.page = page

        # ResetPassword attributes
        self.main_field = CustomTextField(
            label="Correo Electrónico",
            on_change=None
        )
        self.submit_email = CustomElevatedButton(
            name="¡Vamos!",
            width=85,
            bg_color=bgEButtonColor,
            foreground_color=tertiaryTextColor,
            on_click=None,
            border_size=-1
        )

        # Page design
        self.expand = True
        self.bgcolor = bgGeneralFormColor
        self.padding = ft.padding.only(32, 56, 32, 56)

        # Body content
        self.content = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.IconButton(
                            ft.Icons.KEYBOARD_DOUBLE_ARROW_LEFT_ROUNDED,
                            icon_color=primaryCorporateColor,
                            on_click=lambda _: self.page.go("/login"),
                            highlight_color=neutral20,
                            hover_color=neutral10
                        )
                    ]
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        self.main_field, self.submit_email
                    ]
                )
            ]
        )
