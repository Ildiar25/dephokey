import flet as ft

from typing import Callable

from shared.utils.colors import *


class CustomButton(ft.ElevatedButton):
    def __init__(self, text: str, width: int | None = None, on_click: Callable = None) -> None:
        super().__init__()

        # Specific settings
        self.text = text
        self.width = width
        self.on_click = on_click

        # Text design settings
        self.color = textButtonColor
        self.bgcolor = bgButtonColor

        # Button design settings
        self.style = ft.ButtonStyle(
            shape=ft.BeveledRectangleBorder(2)
        )
