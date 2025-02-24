import flet as ft
from enum import Enum

from interface.controls import CustomElevatedButton, ButtonStyle

from shared.utils.colors import *


class FormStyle(Enum):
    ADD = "add"
    EDIT = "edit"


class BaseForm(ft.AlertDialog):
    def __init__(self) -> None:
        super().__init__()

        # General attributes
        self.submit_button = CustomElevatedButton(name="Aceptar", style=ButtonStyle.DEFAULT, disabled=True)
        self.cancel_button = CustomElevatedButton(name="cancelar", style=ButtonStyle.CANCEL)
        self.fields = []

        # Form general settings
        self.modal = True

        # Form general content
        self.actions = [self.cancel_button, self.submit_button]

        # Form general design
        self.shape = ft.RoundedRectangleBorder(4)
        self.bgcolor = bgGeneralFormColor

    def toggle_submit_button_state(self, cursor: ft.ControlEvent) -> None:
        print(cursor.control.value)
        if cursor and all(self.fields):
            self.submit_button.disabled = False
        else:
            self.submit_button.disabled = True
        self.submit_button.update()
