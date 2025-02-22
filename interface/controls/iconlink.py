import flet as ft
from enum import Enum
from typing import Callable, Any

from shared.utils.colors import *


class IconLinkStyle(Enum):
    DARK = "dark"
    LIGHT = "light"


class IconLink(ft.Container):
    def __init__(self, icon: ft.Icons, style: IconLinkStyle, function: Callable[[Any], None] | None = None, **kwargs):
        super().__init__(**kwargs)

        # Sets style & Update
        self.style = style
        self.on_hover = self.toggle_focus_link
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
