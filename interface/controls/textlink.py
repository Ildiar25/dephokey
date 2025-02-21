import flet as ft
from typing import Callable, Any

from shared.utils.colors import *


class TextLink(ft.Container):
    def __init__(self, text: str, function: Callable[[Any], None]) -> None:
        super().__init__()

        # General attributes
        self.content = ft.Text(value=text, color=accentTextColor)

        # Endpoint
        self.on_click = function

        # Style
        self.on_hover = self.toggle_focus_link

    @staticmethod
    def toggle_focus_link(cursor: ft.ControlEvent) -> None:
        if cursor and cursor.control.content.color == accentTextColor:
            cursor.control.content.color = secondaryTextColor
            cursor.control.content.style = ft.TextStyle(
                decoration=ft.TextDecoration.UNDERLINE,
                decoration_color=secondaryTextColor
            )
        else:
            cursor.control.content.color = accentTextColor
            cursor.control.content.style = None
        cursor.control.update()