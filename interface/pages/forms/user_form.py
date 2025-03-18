import flet as ft
from typing import Callable
from types import NoneType
from hashlib import sha256

from data.db_orm import session

from features.models.user import User
from shared.validate import Validate

from .base_form import BaseForm, FormStyle
from interface.controls import CustomTextField

from shared.utils.colors import *


class UserForm(BaseForm):
    def __init__(self, title: str, page: ft.Page, style: FormStyle, user: User,
                 update_changes: Callable[[], None] = None, update_dropdown: Callable[[], None] | None = None) -> None:
        super().__init__()

        # General attributes
        self.page = page
        self.style = style

        # Form attributes
        self.user = user
        self.update_changes = update_changes
        self.update_dropdown = update_dropdown

        # Form fields
        self.u_fullname = CustomTextField(hint_text="Introduce un nombre completo",
            on_change=self.__update_field_inputs, max_length=30)
        self.u_email = CustomTextField(hint_text="Añade un correo electrónico",
            on_change=self.__update_field_inputs, max_length=30)
        self.u_password = CustomTextField(hint_text="Escribe una contraseña",
            on_change=self.__update_field_inputs, max_length=30, password=True, can_reveal_password=True)
        self.u_password_check = CustomTextField(hint_text="Repite la contraseña",
            on_change=self.__update_field_inputs, max_length=30, password=True, can_reveal_password=True)

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

    def __update_field_inputs(self, cursor: ft.ControlEvent) -> None:
        self.u_fullname.reset_error()
        self.fields = [self.u_fullname.value, self.u_email.value, self.u_password.value, self.u_password_check]
        self.toggle_submit_button_state(cursor)

    def __update_appearance(self) -> None:
        match self.style:
            case FormStyle.EDIT:
                self.submit_button.on_click = self.__edit_user
                self.u_fullname.value = self.user.fullname
                self.u_email.value = self.user.email

                self.content.content = ft.Column(
                    spacing=14,
                    controls=[
                        ft.Column(spacing=6, controls=[
                            ft.Text(value="Nombre completo", font_family="AlbertSansR", color=primaryTextColor),
                            self.u_fullname
                        ]),
                        ft.Column(spacing=6, controls=[
                            ft.Text(value="Correo electrónico", font_family="AlbertSansR", color=primaryTextColor,
                                    spans=[self.span]),
                            self.u_email
                        ]),
                        ft.Column(spacing=6, controls=[
                            ft.Text(value="Nueva contraseña", font_family="AlbertSansR", color=primaryTextColor,
                                    spans=[self.span]),
                            self.u_password
                        ]),
                        ft.Column(spacing=6, controls=[
                            ft.Text(value="Repite la contraseña", font_family="AlbertSansR", color=primaryTextColor,
                                    spans=[self.span]),
                            self.u_password_check
                        ])
                    ]
                )

            case _:
                pass

    def __edit_user(self, _: ft.ControlEvent) -> None:

        new_fullname = self.u_fullname.value.strip().title()
        new_email = self.u_email.value.strip().lower()
        new_password = self.u_password.value.strip()
        new_password_check = self.u_password_check.value.strip()

        if not Validate.is_valid_email(new_email):
            self.u_email.show_error("Se necesita un correo válido")
            return
        if not new_password == new_password_check:
            self.u_password.reset_error()
            self.u_password_check.show_error("Las contraseñas no coinciden.")
            return
        if not Validate.is_valid_password(new_password):
            self.u_password_check.reset_error()
            self.u_password.show_error("Contraseña inválida: debe contener mínimo mayúsculas, minúsculas y un número.")
            return

        # Update user-data
        self.user.fullname = new_fullname
        self.user.email = new_email
        self.user.hashed_password = sha256(new_password.encode()).hexdigest()

        session.commit()
        self.update_changes()
        if not isinstance(self.update_dropdown, NoneType):
            self.update_dropdown()
        self.page.close(self)
