import flet as ft

from typing import Callable

from shared.utils.colors import *


class CustomTextButton(ft.TextButton):
    def __init__(self, text: str, on_click: Callable = None) -> None:
        super().__init__()

        # Specific settings
        self.text = text
        self.on_click = on_click

        # Button design settings
        self.style = ft.ButtonStyle(
            color=textColorTextButton,
            overlay_color=overlayColorTextButton
        )
