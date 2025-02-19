import datetime

import flet as ft
from enum import Enum

from data.db_orm import session

from features.models.user import User

from interface.controls import CustomElevatedButton, CustomTextField

from shared.utils.colors import *


class AddFormStyle(Enum):
    CREDITCARD = "creditcard"
    NOTE = "note"
    SITE = "site"


class AddForm(ft.AlertDialog):
    def __init__(self, page: ft.Page, title: str, addform_style: AddFormStyle) -> None:
        super().__init__()

        # General attributes
        self.page = page
        self.addform_style = addform_style
        self.user: User = self.page.session.get("session")
        self.submit_button = CustomElevatedButton(
            name="Aceptar", bg_color=bgEButtonColor, foreground_color=tertiaryTextColor,
            border_size=-1, width=84, disabled=True
        )
        self.cancel_button = CustomElevatedButton(
            name="Cancelar", foreground_color=secondaryTextColor,
            border_size=-1, width=84, on_click=lambda _: self.page.close(self),
        )

        # Content according to style
        match self.addform_style:

            case AddFormStyle.SITE:
                # Site attributes
                self.site_name = CustomTextField(
                    label="Nombre del sitio (opcional)", width=250, on_change=self.toggle_submit_button_state
                )
                self.site_address = CustomTextField(
                    label="Dirección web", prefix_text="http://", width=250, on_change=self.toggle_submit_button_state
                )
                self.site_username = CustomTextField(
                    label="Usuario", width=250, on_change=self.toggle_submit_button_state
                )
                self.site_password = CustomTextField(
                    label="Contraseña", password=True, can_reveal_password=True, width=250,
                    on_change=self.toggle_submit_button_state)

                self.submit_button.on_click = self.add_site

                # Site content
                self.bodycontent = ft.Container(
                    width=524,
                    height=224,
                    content=ft.Column(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Row(
                                wrap=True,
                                controls=[
                                    ft.Text(
                                        value="Todos los siguientes campos son necesarios a no ser que se indique lo "
                                              "contrario. Para añadir un nuevo sitio web a la base de datos, "
                                              "rellena el formulario y pulsa 'Aceptar'.",
                                        font_family="AlbertSansR",
                                        size=16,
                                        color=primaryTextColor
                                    ),
                                ]
                            ),
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[self.site_name, self.site_address]
                            ),
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[self.site_username, self.site_password]
                            )
                        ]
                    )
                )

            case AddFormStyle.CREDITCARD:
                # CreditCard attributes
                self.creditcard_cardholder = CustomTextField(
                    label="Titular", width=250, on_change=self.toggle_submit_button_state
                )
                self.creditcard_alias = CustomTextField(
                    label="Alias (opcional)", width=250, on_change=self.toggle_submit_button_state
                )
                self.creditcard_number = CustomTextField(
                    label="Número", width=320, on_change=self.toggle_submit_button_state
                )
                self.creditcard_cvc = CustomTextField(
                    label="CVC", width=64, on_change=self.toggle_submit_button_state
                )
                self.creditcard_expires_date = CustomTextField(
                    label="Caducidad", width=115, on_change=self.toggle_submit_button_state
                )
                self.submit_button.on_click = self.add_creditcard


                # CreditCard content
                self.bodycontent = ft.Container(
                    width=524,
                    height=224,
                    content=ft.Column(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Row(
                                wrap=True,
                                controls=[
                                    ft.Text(
                                        value="Todos los siguientes campos son necesarios a no ser que se indique lo "
                                              "contrario. Para añadir una nueva tarjeta de crédito a la base de datos, "
                                              "rellena el formulario y pulsa 'Aceptar'.",
                                        font_family="AlbertSansR",
                                        size=16,
                                        color=primaryTextColor
                                    )
                                ]
                            ),
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[self.creditcard_cardholder, self.creditcard_alias]
                            ),
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[self.creditcard_number, self.creditcard_expires_date, self.creditcard_cvc]
                            )
                        ]
                    )
                )

            case AddFormStyle.NOTE:
                # Note attributes
                self.note_title = CustomTextField(
                    label="Título (opcional)", width=520, on_change=self.toggle_submit_button_state
                )
                self.note_content = CustomTextField(
                    label="Contenido", max_lines=2, multiline=True, width=520, min_lines=2,
                    on_change=self.toggle_submit_button_state
                )
                self.submit_button.on_click = self.add_note

                # Note content
                self.bodycontent = ft.Container(
                    width=524,
                    height=224,
                    content=ft.Column(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Row(
                                wrap=True,
                                controls=[
                                    ft.Text(
                                        value="Todos los siguientes campos son necesarios a no ser que se indique lo "
                                              "contrario. Para añadir una nueva nota segura a la base de datos, "
                                              "rellena el formulario y pulsa 'Aceptar'.",
                                        font_family="AlbertSansR",
                                        size=16,
                                        color=primaryTextColor
                                    )
                                ]
                            ),
                            ft.Row(
                                alignment=ft.MainAxisAlignment.CENTER,
                                controls=[self.note_title]
                            ),
                            ft.Row(
                                alignment=ft.MainAxisAlignment.CENTER,
                                controls=[self.note_content]
                            )
                        ]
                    )
                )

            case _:
                self.bodycontent = ft.Text("{nothing_to_show}")

        # Form settings
        self.modal = True

        # F-Title
        self.title = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text(
                    value=title,
                    font_family="AlbertSansB",
                    size=20
                ),
                ft.IconButton(
                    ft.Icons.CLOSE_ROUNDED,
                    icon_color=iconAccentGeneralFormColor,
                    on_click=lambda _: self.page.close(self),
                    highlight_color=selectedIconGeneralFormColor,
                    hover_color=hoverIconGeneralFormColor
                )
            ]
        )

        # F-Content
        self.content = self.bodycontent

        # F-Buttons
        self.actions = [self.cancel_button, self.submit_button]

        # Form design
        self.shape = ft.RoundedRectangleBorder(4)
        self.bgcolor = bgGeneralFormColor

    def toggle_submit_button_state(self, cursor: ft.ControlEvent) -> None:
        # Site status
        if self.addform_style == AddFormStyle.SITE:
            if cursor and all([self.site_address.value, self.site_username.value, self.site_password.value]):
                self.submit_button.disabled = False
            else:
                self.submit_button.disabled = True

        # CreditCard status
        if self.addform_style == AddFormStyle.CREDITCARD:
            if cursor and all([self.creditcard_cardholder.value, self.creditcard_number.value,
                               self.creditcard_cvc.value, self.creditcard_expires_date.value]):
                self.submit_button.disabled = False
            else:
                self.submit_button.disabled = True

        # Note status
        if self.addform_style == AddFormStyle.NOTE:
            if cursor and self.note_content.value:
                self.submit_button.disabled = False
            else:
                self.submit_button.disabled = True
        self.submit_button.update()

    def add_site(self, _: ft.ControlEvent) -> None:
        print("Site added")
        raise NotImplementedError("Implementar 'añadir_sitio_web' a la base de datos.")

    def add_creditcard(self, _: ft.ControlEvent) -> None:
        print("Creditcard added")
        raise NotImplementedError("Implementar 'añadir_tarjeta_de_crédito' a la base de datos.")

    def add_note(self, _: ft.ControlEvent) -> None:
        print("Note added")
        raise NotImplementedError("Implementar 'añadir_nota_segura' a la base de datos.")
