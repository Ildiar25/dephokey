from collections.abc import Callable
from enum import Enum

import flet as ft

from shared.utils.colors import (
    accentTextColor,
    neutral00,
    neutral10,
    neutral20,
    neutral40,
    neutralDangerDark,
    neutralDangerMedium,
    primaryCorporate25,
    primaryCorporateColor,
    secondaryTextColor,
    tertiaryTextColor,
    transparentColor,
)


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
                    ft.ControlState.DISABLED: neutral10,
                    ft.ControlState.DEFAULT: primaryCorporateColor,
                    ft.ControlState.HOVERED: primaryCorporate25,
                    ft.ControlState.FOCUSED: primaryCorporate25
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
                        ft.ControlState.DEFAULT: neutral00,
                        ft.ControlState.DISABLED: neutral00,
                        ft.ControlState.HOVERED: neutral00,
                    },
                    side={
                        ft.ControlState.DEFAULT: ft.BorderSide(
                            width=-1,
                            color=primaryCorporateColor,
                            stroke_align=ft.BorderSideStrokeAlign.INSIDE
                        ),
                        ft.ControlState.HOVERED: ft.BorderSide(
                            width=1.8,
                            color=primaryCorporate25,
                            stroke_align=ft.BorderSideStrokeAlign.INSIDE
                        )
                    },
                    shape=ft.RoundedRectangleBorder(4),
                    elevation=self.elevation
                )

            case ButtonStyle.ICON:
                self.icon=ft.Icons.ADD_ROUNDED
                self.bgcolor = {
                    ft.ControlState.DISABLED: neutral10,
                    ft.ControlState.DEFAULT: primaryCorporateColor,
                    ft.ControlState.HOVERED: primaryCorporate25,
                    ft.ControlState.FOCUSED: primaryCorporate25
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
                        ft.ControlState.DEFAULT: neutral00,
                        ft.ControlState.DISABLED: neutral00,
                        ft.ControlState.HOVERED: neutral00,
                    },
                    side={
                        ft.ControlState.DEFAULT: ft.BorderSide(
                            width=-1,
                            color=primaryCorporateColor,
                            stroke_align=ft.BorderSideStrokeAlign.INSIDE
                        ),
                        ft.ControlState.HOVERED: ft.BorderSide(
                            width=1.8,
                            color=primaryCorporate25,
                            stroke_align=ft.BorderSideStrokeAlign.INSIDE
                        )
                    },
                    shape=ft.RoundedRectangleBorder(4),
                    elevation=self.elevation
                )

            case ButtonStyle.BORDER:
                self.bgcolor = {
                    ft.ControlState.DISABLED: neutral10,
                    ft.ControlState.DEFAULT: transparentColor,
                    ft.ControlState.HOVERED: primaryCorporate25,
                    ft.ControlState.FOCUSED: primaryCorporate25
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
                        ft.ControlState.DEFAULT: primaryCorporateColor,
                        ft.ControlState.DISABLED: neutral00,
                        ft.ControlState.HOVERED: neutral00,
                    },
                    side={
                        ft.ControlState.DEFAULT: ft.BorderSide(
                            width=1.8,
                            color=primaryCorporateColor,
                            stroke_align=ft.BorderSideStrokeAlign.INSIDE
                        ),
                        ft.ControlState.DISABLED: ft.BorderSide(
                            width=1.8,
                            color=neutral20,
                            stroke_align=ft.BorderSideStrokeAlign.INSIDE
                        ),
                        ft.ControlState.HOVERED: ft.BorderSide(
                            width=1.8,
                            color=primaryCorporate25,
                            stroke_align=ft.BorderSideStrokeAlign.INSIDE
                        )
                    },
                    shape=ft.RoundedRectangleBorder(4),
                    elevation=self.elevation
                )

            case ButtonStyle.CANCEL:
                self.bgcolor = {
                    ft.ControlState.DISABLED: neutral10,
                    ft.ControlState.DEFAULT: transparentColor,
                    ft.ControlState.HOVERED: neutral10,
                    ft.ControlState.FOCUSED: neutral10
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
                        ft.ControlState.DEFAULT: neutral40,
                        ft.ControlState.DISABLED: neutral40,
                        ft.ControlState.HOVERED: neutral40,
                    },
                    side={
                        ft.ControlState.DEFAULT: ft.BorderSide(
                            width=-1,
                            color=primaryCorporateColor,
                            stroke_align=ft.BorderSideStrokeAlign.INSIDE
                        ),
                        ft.ControlState.HOVERED: ft.BorderSide(
                            width=1.8,
                            color=neutral10,
                            stroke_align=ft.BorderSideStrokeAlign.INSIDE
                        )
                    },
                    shape=ft.RoundedRectangleBorder(4),
                    elevation=self.elevation
                )

            case ButtonStyle.DELETE:
                self.bgcolor = {
                    ft.ControlState.DISABLED: neutral10,
                    ft.ControlState.DEFAULT: neutralDangerMedium,
                    ft.ControlState.HOVERED: neutralDangerDark,
                    ft.ControlState.FOCUSED: neutralDangerDark
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
                        ft.ControlState.DEFAULT: neutral00,
                        ft.ControlState.DISABLED: neutral00,
                        ft.ControlState.HOVERED: neutral00,
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
