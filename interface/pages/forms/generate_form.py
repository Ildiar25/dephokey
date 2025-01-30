import flet as ft
from enum import Enum

from interface.controls import CustomElevatedButton

from shared.utils.colors import *


class GenerateFormStyle(Enum):
    PASSWORD = "password"
    NUMBER = "number"


class GenerateForm(ft.AlertDialog):
    def __init__(self, page: ft.Page, title: str, generate_style: GenerateFormStyle) -> None:
        super().__init__()

        # General attributes
        self.page = page
        self.generate_style = generate_style

        match generate_style:
            case GenerateFormStyle.PASSWORD:
                self.bodycontent = ft.Container(
                    width=524,
                    height=300
                )

            case GenerateFormStyle.NUMBER:
                self.bodycontent = ft.Container(
                    width = 524,
                    height=150
                )

            case _:
                self.bodycontent = None

        # Form settings
        self.modal = True

        # Form content
        self.title = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text(
                    value=title,
                    font_family="AlbertSansB",
                    size=20
                ),
                ft.IconButton(
                    ft.Icons.CLOSE_ROUNDED,
                    icon_color=iconAccentGeneralFormColor,
                    on_click=lambda _: self.page.close(self),
                    highlight_color=selectedIconGeneralFormColor,
                    hover_color=hoverIconGeneralFormColor
                )
            ]
        )
        self.content = self.bodycontent

        self.actions = [
            CustomElevatedButton(
                name="Generar", bg_color=bgEButtonColor, foreground_color=tertiaryTextColor,
                border_size=-1, expand=True, disabled=True, on_click=self.generate
            )
        ]

        # Form design
        self.shape = ft.RoundedRectangleBorder(4)
        self.bgcolor = bgGeneralFormColor

    def generate(self, _: ft.ControlEvent):
        pass

    @staticmethod
    def create_password(self, min_len: int, max_len: int) -> None:
        pass
