import flet as ft
from enum import Enum

from typing import Callable

from shared.utils.colors import *


class ButtonStyle(Enum):
    DEFAULT = "default"
    ICON = "icon"
    BORDER = "border"
    CANCEL = "cancel"
    DELETE = "delete"


class CustomElevatedButton(ft.ElevatedButton):
    def __init__(
            self, name: str, style: ButtonStyle, on_click: Callable[[ft.ControlEvent], None] | None = None, **kwargs
    ) -> None:
        super().__init__(**kwargs)

        # Specific settings
        self.text = name
        self.on_click = on_click
        self.elevation = 0

        # Create button style
        self.__update_button_appaerance(style)

    def __update_button_appaerance(self, style: ButtonStyle) -> None:
        match style:
            case ButtonStyle.DEFAULT:
                self.bgcolor = {
                    ft.ControlState.DISABLED: bgDissabledEButtonColor,
                    ft.ControlState.DEFAULT: bgEButtonColor,
                    ft.ControlState.HOVERED: bgHoverEButtonColor,
                    ft.ControlState.FOCUSED: bgHoverEButtonColor
                }
                self.style = ft.ButtonStyle(
                    padding={
                        ft.ControlState.DEFAULT: ft.padding.symmetric(vertical=8, horizontal=16),
                        ft.ControlState.DISABLED: ft.padding.symmetric(vertical=8, horizontal=16),
                        ft.ControlState.HOVERED: ft.padding.symmetric(vertical=8, horizontal=16)
                    },
                    color={
                        ft.ControlState.DEFAULT: tertiaryTextColor,
                        ft.ControlState.DISABLED: tertiaryTextColor,
                        ft.ControlState.HOVERED: tertiaryTextColor
                    },
                    icon_color={
                        ft.ControlState.DEFAULT: tertiaryIconColor,
                        ft.ControlState.DISABLED: tertiaryIconColor,
                        ft.ControlState.HOVERED: tertiaryIconColor,
                    },
                    side={
                        ft.ControlState.DEFAULT: ft.BorderSide(
                            width=-1,
                            color=borderEButtonColor,
                            stroke_align=ft.BorderSideStrokeAlign.INSIDE
                        ),
                        ft.ControlState.HOVERED: ft.BorderSide(
                            width=1.8,
                            color=bgHoverEButtonColor,
                            stroke_align=ft.BorderSideStrokeAlign.INSIDE
                        )
                    },
                    shape=ft.RoundedRectangleBorder(4),
                    elevation=self.elevation
                )

            case ButtonStyle.ICON:
                self.icon=ft.Icons.ADD_ROUNDED
                self.bgcolor = {
                    ft.ControlState.DISABLED: bgDissabledEButtonColor,
                    ft.ControlState.DEFAULT: bgEButtonColor,
                    ft.ControlState.HOVERED: bgHoverEButtonColor
                }
                self.style = ft.ButtonStyle(
                    padding={
                        ft.ControlState.DEFAULT: ft.padding.symmetric(vertical=8, horizontal=16),
                        ft.ControlState.DISABLED: ft.padding.symmetric(vertical=8, horizontal=16),
                        ft.ControlState.HOVERED: ft.padding.symmetric(vertical=8, horizontal=16)
                    },
                    color={
                        ft.ControlState.DEFAULT: tertiaryTextColor,
                        ft.ControlState.DISABLED: tertiaryTextColor,
                        ft.ControlState.HOVERED: tertiaryTextColor
                    },
                    icon_color={
                        ft.ControlState.DEFAULT: tertiaryIconColor,
                        ft.ControlState.DISABLED: tertiaryIconColor,
                        ft.ControlState.HOVERED: tertiaryIconColor,
                    },
                    side={
                        ft.ControlState.DEFAULT: ft.BorderSide(
                            width=-1,
                            color=borderEButtonColor,
                            stroke_align=ft.BorderSideStrokeAlign.INSIDE
                        ),
                        ft.ControlState.HOVERED: ft.BorderSide(
                            width=1.8,
                            color=bgHoverEButtonColor,
                            stroke_align=ft.BorderSideStrokeAlign.INSIDE
                        )
                    },
                    shape=ft.RoundedRectangleBorder(4),
                    elevation=self.elevation
                )

            case ButtonStyle.BORDER:
                self.bgcolor = {
                    ft.ControlState.DISABLED: bgDissabledEButtonColor,
                    ft.ControlState.DEFAULT: transparentColor,
                    ft.ControlState.HOVERED: bgHoverEButtonColor
                }
                self.style = ft.ButtonStyle(
                    padding={
                        ft.ControlState.DEFAULT: ft.padding.symmetric(vertical=8, horizontal=16),
                        ft.ControlState.DISABLED: ft.padding.symmetric(vertical=8, horizontal=16),
                        ft.ControlState.HOVERED: ft.padding.symmetric(vertical=8, horizontal=16)
                    },
                    color={
                        ft.ControlState.DEFAULT: accentTextColor,
                        ft.ControlState.DISABLED: tertiaryTextColor,
                        ft.ControlState.HOVERED: tertiaryTextColor
                    },
                    icon_color={
                        ft.ControlState.DEFAULT: accentIconColor,
                        ft.ControlState.DISABLED: tertiaryIconColor,
                        ft.ControlState.HOVERED: tertiaryIconColor,
                    },
                    side={
                        ft.ControlState.DEFAULT: ft.BorderSide(
                            width=1.8,
                            color=borderEButtonColor,
                            stroke_align=ft.BorderSideStrokeAlign.INSIDE
                        ),
                        ft.ControlState.DISABLED: ft.BorderSide(
                            width=1.8,
                            color=borderDissabledEButtonColor,
                            stroke_align=ft.BorderSideStrokeAlign.INSIDE
                        ),
                        ft.ControlState.HOVERED: ft.BorderSide(
                            width=1.8,
                            color=borderHoverEButtonColor,
                            stroke_align=ft.BorderSideStrokeAlign.INSIDE
                        )
                    },
                    shape=ft.RoundedRectangleBorder(4),
                    elevation=self.elevation
                )

            case ButtonStyle.CANCEL:
                self.bgcolor = {
                    ft.ControlState.DISABLED: bgDissabledEButtonColor,
                    ft.ControlState.DEFAULT: transparentColor,
                    ft.ControlState.HOVERED: bgDissabledEButtonColor
                }
                self.style = ft.ButtonStyle(
                    padding={
                        ft.ControlState.DEFAULT: ft.padding.symmetric(vertical=8, horizontal=16),
                        ft.ControlState.DISABLED: ft.padding.symmetric(vertical=8, horizontal=16),
                        ft.ControlState.HOVERED: ft.padding.symmetric(vertical=8, horizontal=16)
                    },
                    color={
                        ft.ControlState.DEFAULT: secondaryTextColor,
                        ft.ControlState.DISABLED: secondaryTextColor,
                        ft.ControlState.HOVERED: secondaryTextColor
                    },
                    icon_color={
                        ft.ControlState.DEFAULT: secondaryIconColor,
                        ft.ControlState.DISABLED: secondaryIconColor,
                        ft.ControlState.HOVERED: secondaryIconColor,
                    },
                    side={
                        ft.ControlState.DEFAULT: ft.BorderSide(
                            width=-1,
                            color=borderEButtonColor,
                            stroke_align=ft.BorderSideStrokeAlign.INSIDE
                        ),
                        ft.ControlState.HOVERED: ft.BorderSide(
                            width=1.8,
                            color=bgDissabledEButtonColor,
                            stroke_align=ft.BorderSideStrokeAlign.INSIDE
                        )
                    },
                    shape=ft.RoundedRectangleBorder(4),
                    elevation=self.elevation
                )

            case ButtonStyle.DELETE:
                self.bgcolor = {
                    ft.ControlState.DISABLED: bgDissabledEButtonColor,
                    ft.ControlState.DEFAULT: neutralDangerMedium,
                    ft.ControlState.HOVERED: neutralDangerDark
                }
                self.style = ft.ButtonStyle(
                    padding={
                        ft.ControlState.DEFAULT: ft.padding.symmetric(vertical=8, horizontal=16),
                        ft.ControlState.DISABLED: ft.padding.symmetric(vertical=8, horizontal=16),
                        ft.ControlState.HOVERED: ft.padding.symmetric(vertical=8, horizontal=16)
                    },
                    color={
                        ft.ControlState.DEFAULT: tertiaryTextColor,
                        ft.ControlState.DISABLED: tertiaryTextColor,
                        ft.ControlState.HOVERED: tertiaryTextColor
                    },
                    icon_color={
                        ft.ControlState.DEFAULT: tertiaryIconColor,
                        ft.ControlState.DISABLED: tertiaryIconColor,
                        ft.ControlState.HOVERED: tertiaryIconColor,
                    },
                    side={
                        ft.ControlState.DEFAULT: ft.BorderSide(
                            width=-1,
                            color=neutralDangerDark,
                            stroke_align=ft.BorderSideStrokeAlign.INSIDE
                        ),
                        ft.ControlState.HOVERED: ft.BorderSide(
                            width=2,
                            color=neutralDangerDark,
                            stroke_align=ft.BorderSideStrokeAlign.INSIDE
                        )
                    },
                    shape=ft.RoundedRectangleBorder(4),
                    elevation=self.elevation
                )
