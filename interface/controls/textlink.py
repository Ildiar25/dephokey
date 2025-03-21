from collections.abc import Callable
from typing import Any

import flet as ft

from shared.utils.colors import accentTextColor, secondaryTextColor


class TextLink(ft.Container):
    """Creates a clickable text."""
    def __init__(self, text: str, target: Callable[[Any], None], **kwargs) -> None:
        super().__init__(**kwargs)

        # General attributes
        self.content = ft.Text(value=text, color=accentTextColor)

        # Endpoint
        self.on_click = target

        # Style
        self.on_hover = self.__toggle_focus_link

    @staticmethod
    def __toggle_focus_link(cursor: ft.ControlEvent) -> None:
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
