from enum import Enum

import flet as ft

from interface.controls import CustomElevatedButton
from interface.controls.e_button import ButtonStyle
from shared.utils.colors import (
    dangerTextColor,
    neutral00,
    neutral20,
    neutral40,
    neutral80,
)


class FormStyle(Enum):
    ADD = "add"
    EDIT = "edit"
    RESET = "reset"
    PASSWORD = "password"
    CC_NUMBER = "cc_number"


class BaseForm(ft.AlertDialog):
    def __init__(self) -> None:
        super().__init__()

        # General attributes
        self.fields = []
        self.submit_button = CustomElevatedButton(name="Aceptar", style=ButtonStyle.DEFAULT, disabled=True)
        self.cancel_button = CustomElevatedButton(name="Cancelar", style=ButtonStyle.CANCEL)
        self.span = ft.TextSpan(text="*", style=ft.TextStyle(font_family="AlbertSansB", color=dangerTextColor))
        self.close_button = ft.IconButton(
            ft.Icons.CLOSE_ROUNDED, icon_color=neutral80, on_click=lambda _: self.page.close(self),
            highlight_color=neutral40, hover_color=neutral20
        )

        # Form general settings
        self.modal = True

        # Form general content
        self.content = ft.Container(width=550, height=378)
        self.actions = [self.cancel_button, self.submit_button]

        # Form general design
        self.shape = ft.RoundedRectangleBorder(4)
        self.bgcolor = neutral00

    def toggle_submit_button_state(self, cursor: ft.ControlEvent) -> None:
        if cursor and all(self.fields):
            self.submit_button.disabled = False
        else:
            self.submit_button.disabled = True
        self.submit_button.update()
