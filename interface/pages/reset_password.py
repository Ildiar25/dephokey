import flet as ft

from shared.utils.colors import *


class ResetPasswordPage(ft.Container):
    def __init__(self, page: ft.Page) -> None:
        super().__init__()

        # General attributes
        self.page = page

        # ResetPassword attributes

        # Page design
        self.expand = True
        self.bgcolor = bgGeneralFormColor
        self.padding = ft.padding.only(32, 56, 32)

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
                )
            ]
        )
