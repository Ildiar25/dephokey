import flet as ft

from shared.utils.colors import *


class CustomSwitch(ft.Container):
    def __init__(self, title: str, width: int) -> None:
        super().__init__()

        self.width = width

        self.content = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text(
                    title,
                    color=secondaryTextColor,
                    size=16
                ),
                ft.Switch(
                    width=36,
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