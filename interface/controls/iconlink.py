import time
from collections.abc import Callable
from enum import Enum
from typing import Any

import flet as ft

from shared.utils.colors import (
accentIconColor,
neutralSuccessLight,
primaryIconColor,
secondaryIconColor,
successTextColor,
tertiaryIconColor,
)


class IconLinkStyle(Enum):
    DARK = "dark"
    LIGHT = "light"


class IconLink(ft.Container):
    def __init__(self, icon: ft.Icons, style: IconLinkStyle, function: Callable[[Any], None] | None = None, **kwargs):
        super().__init__(**kwargs)

        # Sets style & Update
        self.style = style
        self.on_hover = self.toggle_focus_link
        self.badge = ft.Badge(
            bgcolor=neutralSuccessLight, text_color=successTextColor, offset=ft.Offset(-25, -20),
            label_visible=False, padding=ft.padding.symmetric(horizontal=10),
            text_style=ft.TextStyle(font_family="AlbertSansR", size=12)
        )
        self.__update_appareance(icon)

        # Endpoint
        self.on_click = function

    def __update_appareance(self, icon: ft.Icons) -> None:
        match self.style:
            case IconLinkStyle.LIGHT:
                self.content = ft.Icon(name=icon, color=accentIconColor)

            case IconLinkStyle.DARK:
                self.content = ft.Icon(name=icon, color=tertiaryIconColor)

    def toggle_focus_link(self, cursor: ft.ControlEvent) -> None:
        match self.style:
            case IconLinkStyle.LIGHT:
                if cursor and cursor.control.content.color == accentIconColor:
                    cursor.control.content.color = primaryIconColor
                else:
                    cursor.control.content.color = accentIconColor
                cursor.control.update()

            case IconLinkStyle.DARK:
                if cursor and cursor.control.content.color == tertiaryIconColor:
                    cursor.control.content.color = secondaryIconColor
                else:
                    cursor.control.content.color = tertiaryIconColor
                cursor.control.update()

    def show_badge(self, msg: str  = "¡copiado!") -> None:
        self.badge.text = msg
        self.badge.label_visible = True
        self.update()
        time.sleep(1)
        self.badge.label_visible = False
        self.update()
