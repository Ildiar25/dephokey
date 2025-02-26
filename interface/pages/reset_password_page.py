import flet as ft

from interface.pages.forms.base_form import FormStyle
from interface.pages.forms import ChangePasswordForm
from interface.controls import *

from shared.utils.colors import *


class ResetPasswordPage(ft.Container):
    def __init__(self, page: ft.Page) -> None:
        super().__init__()

        # General attributes
        self.page = page
        self.snackbar = Snackbar()

        # ResetPassword attributes
        self.main_field = CustomTextField(label="Correo Electrónico", on_change=None)
        self.submit_email = CustomElevatedButton(name="¡Vamos!", style=ButtonStyle.DEFAULT, on_click=self.open_form)

        # Page design
        self.expand = True
        self.bgcolor = bgGeneralFormColor
        self.padding = ft.padding.symmetric(vertical=56, horizontal=32)

        # Body content
        self.content = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.IconButton(
                            ft.Icons.KEYBOARD_DOUBLE_ARROW_LEFT_ROUNDED,
                            icon_color=primaryCorporateColor,
                            on_click=lambda _: self.page.go("/login"),
                            highlight_color=neutral20,
                            hover_color=neutral10
                        )
                    ]
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        self.main_field, self.submit_email, self.snackbar
                    ]
                )
            ]
        )

    def open_form(self, _: ft.ControlEvent) -> None:
        self.page.open(
            ChangePasswordForm(self.page, self.snackbar, FormStyle.RESET, self.main_field.value)
        )
