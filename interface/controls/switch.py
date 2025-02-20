import flet as ft
from typing import Callable

from shared.utils.colors import *


class CustomSwitch(ft.Container):
    def __init__(self, title: str, width: int | None = None, expand: bool = False,
                 on_change: Callable[[ft.ControlEvent], None] | None = None, value: bool = False) -> None:
        super().__init__()

        self.width = width
        self.expand = expand

        self.content = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text(
                    title,
                    color=secondaryTextColor,
                    size=16
                ),
                ft.Switch(
                    value=value,
                    width=36,
                    on_change=on_change,
                    active_track_color=neutralSuccessMedium,
                    track_color={
                        ft.ControlState.PRESSED: ft.Colors.PINK
                    }
                )
            ]
        )

    def get_value(self) -> bool:
        return self.content.controls[1].value

    def set_value(self, value: bool) -> None:
        self.content.controls[1].value = value