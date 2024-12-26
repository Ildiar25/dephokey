import flet as ft

from typing import Callable

from shared.utils.colors import *


class CustomElevatedButton(ft.ElevatedButton):
    def __init__(self, text: str, width: int | None = None, on_click: Callable = None,
                 disabled: bool | None = None) -> None:
        super().__init__()

        # Specific settings
        self.text = text
        self.width = width
        self.on_click = on_click
        self.disabled = disabled

        # Text design settings
        self.color = textColorElevatedButton

        self.bgcolor = {
            ft.ControlState.DISABLED: bgDissabledButtonColor,
            ft.ControlState.DEFAULT: bgButtonColor
        }

        # Button design settings
        self.style = ft.ButtonStyle(
            text_style=ft.TextStyle(
                font_family="AlbertSansB"
            ),
            shape=ft.BeveledRectangleBorder(2)
        )
