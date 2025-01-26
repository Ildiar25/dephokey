import flet as ft

from typing import Callable, Union

from shared.utils.colors import *


class CustomElevatedButton(ft.ElevatedButton):
    def __init__(self, name: str, width: int, icon: ft.Icons | None = None,
                 foreground_color: Union[str, ft.Colors] | None = None,
                 bg_color: Union[str, ft.Colors] | None = None,
                 on_click: Callable[[ft.ControlEvent], None] | None = None,
                 disabled: bool = False, border_size: int | None = None) -> None:
        super().__init__()

        # Specific settings
        self.text = name
        self.icon = icon
        self.width = width
        self.on_click = on_click
        self.disabled = disabled
        self.elevation = 0

        # Button design settings
        self.bgcolor = {
            ft.ControlState.DISABLED: dissabledEButtonColor,
            ft.ControlState.DEFAULT: bg_color,
            ft.ControlState.HOVERED: primaryCorporate25
        }
        self.style = ft.ButtonStyle(
            text_style=ft.TextStyle(
                font_family="AlbertSansL"
            ),
            color={
                ft.ControlState.DEFAULT: foreground_color,
                ft.ControlState.DISABLED: foreground_color,
                ft.ControlState.HOVERED: neutral00
            },
            icon_color={
                ft.ControlState.DEFAULT: foreground_color,
                ft.ControlState.DISABLED: foreground_color,
                ft.ControlState.HOVERED: neutral00,
            },
            side={
                ft.ControlState.DEFAULT: ft.BorderSide(
                    width=border_size,
                    color=borderEButtonColor,
                    stroke_align=ft.BorderSideStrokeAlign.INSIDE
                ),
                ft.ControlState.HOVERED: ft.BorderSide(
                    width=2,
                    color=primaryCorporate25,
                    stroke_align=ft.BorderSideStrokeAlign.INSIDE
                )
            },
            shape=ft.RoundedRectangleBorder(4),
            elevation=self.elevation
        )
