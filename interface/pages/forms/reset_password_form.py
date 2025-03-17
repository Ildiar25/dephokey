import flet as ft
from typing import Callable
from types import NoneType

from data.db_orm import session

from features.data_encryption.core import decrypt_data, encrypt_data
from features.models import PasswordRequest

from .base_form import BaseForm, FormStyle
from interface.controls import CustomTextField

from shared.utils.colors import *


class ResetPasswordForm(BaseForm):
    def __init__(self, title: str, page: ft.Page, style: FormStyle, password_request: PasswordRequest | None = None,
                 update_changes: Callable[[], None] = None, update_dropdown: Callable[[], None] | None = None) -> None:
        super().__init__()

        # General attributes
        self.page = page
        self.style = style

        # Form attributes
        self.password_request = password_request
        self.update_changes = update_changes
        self.update_dropdown = update_dropdown

        # Form fields
        self.pr_token = CustomTextField(
            hint_text="Introduce un nuevo token", max_length=7, can_reveal_password=True, password=True,
            on_change=self.__update_field_inputs
        )

        # Form settings
        self.cancel_button.on_click = lambda _: self.page.close(self)

        # Form title
        self.title = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text(title, font_family="AlbertSansB", size=20, color=primaryTextColor), self.close_button
            ]
        )

        self.__update_appearance()

    def __update_appearance(self) -> None:
        match self.style:
            case FormStyle.EDIT:
                self.submit_button.on_click = self.__edit_password_request
                self.pr_token.value = decrypt_data(self.password_request.encrypted_code)

                # Content
                self.content.content = ft.Column(
                    spacing=14,
                    controls=[
                        ft.Column(spacing=6, controls=[
                            ft.Text(value="Nuevo token", font_family="AlbertSansR", color=primaryTextColor),
                            self.pr_token
                        ])
                    ]
                )

            case _:
                pass

    def __update_field_inputs(self, cursor: ft.ControlEvent) -> None:
        self.pr_token.reset_error()
        self.fields = [self.pr_token]
        self.toggle_submit_button_state(cursor)

    def __edit_password_request(self, _: ft.ControlEvent) -> None:

        new_token = self.pr_token.value.strip().upper()

        if not len(new_token) == 7:
            self.pr_token.show_error("El token necesita 7 caracteres.")
            return

        # Update token-data
        self.password_request.encrypted_code = encrypt_data(new_token)

        session.commit()
        self.update_changes()
        if not isinstance(self.update_dropdown, NoneType):
            self.update_dropdown()
        self.page.close(self)
