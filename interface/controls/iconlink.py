import time
from collections.abc import Callable
from enum import Enum
from typing import Any

import flet as ft

from shared.utils.colors import (
    neutral00,
    neutral40,
    neutral80,
    neutralSuccessLight,
    primaryCorporateColor,
    successTextColor,
)


class IconLinkStyle(Enum):
    DARK = "dark"
    LIGHT = "light"


class IconLink(ft.Container):
    """Creates a custom clickable icon image according to a given ICON STYLE."""
    def __init__(self, icon: ft.Icons, style: IconLinkStyle, target: Callable[[Any], None] | None = None, **kwargs):
        super().__init__(**kwargs)

        # Sets style & Update
        self.style = style
        self.on_hover = self.__toggle_focus_link
        self.badge = ft.Badge(
            bgcolor=neutralSuccessLight,
            text_color=successTextColor,
            offset=ft.Offset(-25, -20),
            label_visible=False,
            padding=ft.padding.symmetric(horizontal=10),
            text_style=ft.TextStyle(font_family="AlbertSansR", size=12)
        )
        self.__update_appareance(icon)

        # Endpoint
        self.on_click = target

    def __update_appareance(self, icon: ft.Icons) -> None:
        match self.style:
            case IconLinkStyle.LIGHT:
                self.content = ft.Icon(name=icon, color=primaryCorporateColor)

            case IconLinkStyle.DARK:
                self.content = ft.Icon(name=icon, color=neutral00)

    def __toggle_focus_link(self, cursor: ft.ControlEvent) -> None:
        match self.style:
            case IconLinkStyle.LIGHT:
                if cursor and cursor.control.content.color == primaryCorporateColor:
                    cursor.control.content.color = neutral80
                else:
                    cursor.control.content.color = primaryCorporateColor

                cursor.control.update()

            case IconLinkStyle.DARK:
                if cursor and cursor.control.content.color == neutral00:
                    cursor.control.content.color = neutral40
                else:
                    cursor.control.content.color = neutral00

                cursor.control.update()

    def show_badge(self, msg: str  = "¡copiado!") -> None:
        self.badge.text = msg
        self.badge.label_visible = True
        self.update()
        time.sleep(1)
        self.badge.label_visible = False
        self.update()
