import flet as ft
from typing import Callable

from data.db_orm import session

from features.encryption.core import decrypt_data, encrypt_data
from features.models.user import User
from features.models import Site

from .base_form import BaseForm, FormStyle
from interface.controls import CustomTextField, Snackbar, SnackbarStyle

from shared.validate import Validate
from shared.utils.colors import *


class SiteForm(BaseForm):
    def __init__(self,
                 title: str, page: ft.Page, style: FormStyle, snackbar: Snackbar | None = None,
                 site: Site | None = None, update_changes: Callable[[], None] = None) -> None:
        super().__init__()

        # General attributes
        self.page = page
        self.snackbar = snackbar
        self.style = style
        self.site = site
        self.update_changes = update_changes

        # Form attributes
        self.user: User = self.page.session.get("session")

        # Form fields
        self.s_name = CustomTextField(hint_text="Dale un nombre a la dirección web",
            on_change=self.__update_field_inputs, max_length=30)
        self.s_address = CustomTextField(hint_text="Escribe la dirección", max_length=50,
            prefix_style=ft.TextStyle(color=primaryTextColor), on_change=self.__update_field_inputs)
        self.s_username = CustomTextField(hint_text="Añade el usuario con el que te has registrado",
            on_change=self.__update_field_inputs, max_length=30)
        self.s_password = CustomTextField(hint_text="Escribe la contraseña", max_length=30,
            on_change=self.__update_field_inputs, password=True, can_reveal_password=True)

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
            case FormStyle.ADD:
                self.submit_button.on_click = self.__add_site
                self.s_address.prefix_text = "http://"

                # Content
                self.content.content = ft.Column(
                    spacing=14,
                    controls=[
                        ft.Column(spacing=6, controls=[
                            ft.Text(value="Nombre", font_family="AlbertSansR", color=primaryTextColor),
                            self.s_name
                        ]),
                        ft.Column(spacing=6, controls=[
                            ft.Text(value="Dirección", font_family="AlbertSansR", color=primaryTextColor,
                                    spans=[self.span]),
                            self.s_address
                        ]),
                        ft.Column(spacing=6, controls=[
                            ft.Text(value="Usuario", font_family="AlbertSansR", color=primaryTextColor,
                                    spans=[self.span]),
                            self.s_username
                        ]),
                        ft.Column(spacing=6, controls=[
                            ft.Text(value="Contraseña", font_family="AlbertSansR", color=primaryTextColor,
                                    spans=[self.span]),
                            self.s_password
                        ])
                    ]
                )

            case FormStyle.EDIT:
                self.submit_button.on_click = self.__update_site
                self.s_name.value = self.site.name
                self.s_address.value = self.site.address
                self.s_address.prefix_text = None
                self.s_username.value = self.site.username
                self.s_password.value = decrypt_data(self.site.encrypted_password)

                # Content
                self.content.content = ft.Column(
                    spacing=14,
                    controls=[
                        ft.Column(spacing=6, controls=[
                            ft.Text(value="Nombre", font_family="AlbertSansR", color=primaryTextColor),
                            self.s_name
                        ]),
                        ft.Column(spacing=6, controls=[
                            ft.Text(value="Dirección", font_family="AlbertSansR", color=primaryTextColor,
                                    spans=[self.span]),
                            self.s_address
                        ]),
                        ft.Column(spacing=6, controls=[
                            ft.Text(value="Usuario", font_family="AlbertSansR", color=primaryTextColor,
                                    spans=[self.span]),
                            self.s_username
                        ]),
                        ft.Column(spacing=6, controls=[
                            ft.Text(value="Contraseña", font_family="AlbertSansR", color=primaryTextColor,
                                    spans=[self.span]),
                            self.s_password
                        ])
                    ]
                )

    def __update_field_inputs(self, cursor: ft.ControlEvent) -> None:
        self.s_address.reset_error()
        self.fields = [self.s_address.value, self.s_username.value, self.s_password.value]
        self.toggle_submit_button_state(cursor)

    @staticmethod
    def rename_address(new_address: str) -> str:
        address = ""
        if not new_address.startswith(("http://", "https://")):
            address = "http://"
        address += new_address
        if not new_address.endswith("/"):
            address += "/"
        return address

    def __update_site(self, _: ft.ControlEvent) -> None:

        new_name = self.s_name.value.capitalize().strip() if self.s_name.value else "Nueva dirección web"
        new_address = self.rename_address(self.s_address.value.strip())
        new_username = self.s_username.value.strip()
        new_password = self.s_password.value.strip()

        if not Validate.is_valid_address(new_address):
            self.s_address.show_error("No es una dirección válida.")
            return

        # Update site-data
        self.site.name = new_name
        self.site.address = new_address
        self.site.username = new_username
        self.site.encrypted_password = encrypt_data(new_password)

        session.commit()
        self.update_changes()
        self.page.close(self)

    def __add_site(self, _: ft.ControlEvent) -> None:

        new_name = self.s_name.value.capitalize().strip() if self.s_name.value else "Nueva dirección web"
        new_address = self.rename_address(self.s_address.value.strip())
        new_username = self.s_username.value.strip()
        new_password = self.s_password.value.strip()

        if not Validate.is_valid_address(new_address):
            self.s_address.show_error("No es una dirección válida.")
            return

        # Create new site-instance
        new_site = Site(new_address, new_username, new_password, self.user, new_name)
        session.add(new_site)
        session.commit()

        self.update_changes()
        self.snackbar.change_style(msg=f"¡{new_name} añadida!", style=SnackbarStyle.SUCCESS)
        self.snackbar.update()
        self.page.close(self)
