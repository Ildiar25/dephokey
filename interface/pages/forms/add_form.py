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
            border_size=-1, width=84, disabled=False
        )
        self.cancel_button = CustomElevatedButton(
            name="Cancelar", foreground_color=secondaryTextColor,
            border_size=-1, width=84, on_click=lambda _: self.page.close(self),
        )

        # Content according to style
        match self.addform_style:

            case AddFormStyle.SITE:
                # Site attributes
                self.site_name = CustomTextField(label="Nombre del sitio (opcional)", width=250)
                self.site_address = CustomTextField(label="Dirección web", prefix_text="http://", width=250)
                self.site_username = CustomTextField(label="Usuario", width=250)
                self.site_password = CustomTextField(label="Contraseña", password=True, can_reveal_password=True,
                                                     width=250)

                self.submit_button.on_click = lambda _:print(self.site_address.value)

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
                self.creditcard_cardholder = CustomTextField(label="Titular", width=250)
                self.creditcard_alias = CustomTextField(label="Alias (opcional)", width=250)
                self.creditcard_number = CustomTextField(label="Número", width=350)
                self.creditcard_cvc = CustomTextField(label="CVC", width=64)
                self.creditcard_expires_date = CustomTextField(label="Caducidad", width=400)
                self.date_button = ft.IconButton(
                    ft.Icons.CALENDAR_MONTH_ROUNDED,
                    icon_color=primaryCorporateColor,
                    highlight_color=selectedIconGeneralFormColor,
                    hover_color=hoverIconGeneralFormColor,
                    tooltip="Seleccionar fecha"
                )

                # CreditCard content
                self.bodycontent = ft.Container(
                    width=524,
                    height=304,
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
                                controls=[self.creditcard_number, self.creditcard_cvc]
                            ),
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[self.creditcard_expires_date, self.date_button]
                            )
                        ]
                    )
                )

            case AddFormStyle.NOTE:
                # Note attributes

                # Note content
                self.bodycontent = ft.Text("NOTE CONTENT")

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

    def update_creditcard_date(self, new_date: datetime.datetime) -> None:
        pass