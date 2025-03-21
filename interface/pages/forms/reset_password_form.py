from collections.abc import Callable
from types import NoneType

import flet as ft

from data.db_orm import session
from features.data_encryption.core import decrypt_data, encrypt_data
from features.models import PasswordRequest
from interface.controls import CustomTextField
from shared.utils.colors import primaryTextColor

from .base_form import BaseForm, FormStyle


class ResetPasswordForm(BaseForm):
    """Creates a form to edit token data."""
    def __init__(
            self,
            title: str,
            page: ft.Page,
            style: FormStyle,
            password_request: PasswordRequest | None = None,
            update_changes: Callable[[], None] = None,
            update_dropdown: Callable[[], None] | None = None
    ) -> None:
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
            hint_text="Introduce un nuevo token",
            max_length=7,
            can_reveal_password=True,
            password=True,
            on_change=self.__update_field_inputs
        )

        # Form settings
        self.cancel_button.on_click = lambda _: self.page.close(self)

        # Form title
        self.title = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text(title, font_family="AlbertSansB", size=20, color=primaryTextColor),
                self.close_button,
            ]
        )

        self.__update_appearance()

    def __update_appearance(self) -> None:
        match self.style:
            case FormStyle.EDIT:
                self.content = ft.Container(width=524, height=150)
                self.submit_button.on_click = self.__edit_token
                self.pr_token.on_submit = self.__edit_token
                self.pr_token.value = decrypt_data(self.password_request.encrypted_code)

                # Content
                self.content.content = ft.Column(
                    spacing=14,
                    controls=[
                        ft.Row(
                            wrap=True,
                            controls=[
                                ft.Text(
                                    value="Para cambiar el token actual introduce una serie de números y letras "
                                          "aleatoriass (A-Z) que formen un total de siete caracteres.",
                                    font_family="AlbertSansR",
                                    color=primaryTextColor,
                                    size=16
                                )
                            ]
                        ),
                        ft.Column(
                            spacing=6,
                            controls=[
                                ft.Text(value="Nuevo token", font_family="AlbertSansR", color=primaryTextColor),
                                self.pr_token,
                            ]
                        ),
                    ]
                )

            case _:
                pass

    def __update_field_inputs(self, cursor: ft.ControlEvent) -> None:
        self.pr_token.reset_error()
        self.fields = [self.pr_token]
        self._toggle_submit_button_state(cursor)

    def __edit_token(self, _: ft.ControlEvent) -> None:
        new_token = self.pr_token.value.strip().upper()

        if len(new_token) != 7:
            self.pr_token.show_error("El token debe ser de 7 caracteres.")
            return

        # Update token-data
        self.password_request.encrypted_code = encrypt_data(new_token)

        self.__save_changes()
        self.page.close(self)

    def __save_changes(self):
        session.commit()

        self.update_changes()
        if not isinstance(self.update_dropdown, NoneType):
            self.update_dropdown()
