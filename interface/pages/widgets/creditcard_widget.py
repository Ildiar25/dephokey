import textwrap
from collections.abc import Callable
from enum import Enum

import flet as ft

from features.data_encryption.core import decrypt_data
from features.models import CreditCard
from interface.controls import IconLink
from interface.controls.iconlink import IconLinkStyle
from interface.pages.forms import CreditCardForm, DeleteForm
from interface.pages.forms.base_form import FormStyle
from interface.pages.forms.delete_form import DeleteFormStyle
from shared.utils.colors import (
    neutral00,
    neutral20,
    neutralDangerDark,
    neutralDangerMedium,
    primaryCorporate100,
    primaryCorporateColor,
    tertiaryTextColor,
)
from shared.utils.masker import mask_number


class CreditCardStyle(Enum):
    FRONT = "front"
    BACK = "back"


class CreditCardWidget(ft.Card):
    """This class displays all creditcard data"""
    def __init__(self, creditcard: CreditCard, page: ft.Page, update_appearance: Callable[[], None]) -> None:
        super().__init__()

        # General attributes
        self.creditcard = creditcard
        self.page = page
        self.update_appearance = update_appearance
        self.style = CreditCardStyle.FRONT

        # Widget settings
        self.width = 365
        self.height = 225
        self.elevation = 2
        self.animate_scale = ft.animation.Animation(200, ft.AnimationCurve.EASE_IN_OUT)

        # CreditCardWidget elements
        self.card_alias = ft.Text(
            value=self.creditcard.alias if self.creditcard.alias else "Alias",
            font_family="AlbertSansB",
            size=18,
            color=tertiaryTextColor
        )
        self.card_number = ft.Row(
            spacing=18,
            expand=True,
            controls=[
                ft.Text(
                    value=group,
                    font_family="IcelandR",
                    color=tertiaryTextColor,
                    size=20
                ) for group in textwrap.wrap(decrypt_data(self.creditcard.encrypted_number), width=4)
            ]
        )
        self.card_cvc = ft.Text(
            mask_number(decrypt_data(self.creditcard.encrypted_cvc)), font_family="AlbertSansB", size=16
        )

        # Widget design
        self.color = primaryCorporateColor if not self.creditcard.expired else neutralDangerMedium
        self.shape = ft.RoundedRectangleBorder(24)
        self.tooltip = "Clickea para voltear la tarjeta"

        # Widget content
        self.front_content = ft.Container(
            padding=ft.padding.all(24),
            content=ft.Column(
                spacing=20,
                controls=[
                    # Header
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            self.card_alias,
                            ft.Container(
                                content=ft.Row(
                                    spacing=8,
                                    controls=[
                                        IconLink(
                                            icon=ft.Icons.EDIT_OUTLINED,
                                            style=IconLinkStyle.DARK,
                                            target=self.__open_edit_creditcard_form
                                        ),
                                        IconLink(
                                            icon=ft.Icons.DELETE_OUTLINED,
                                            style=IconLinkStyle.DARK,
                                            target=self.__open_delete_form
                                        ),
                                    ]
                                )
                            ),
                        ]
                    ),
                    # Body
                    ft.Image(src=r"interface\assets\creditcard-chip.svg", height=29),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            self.card_number,
                            IconLink(
                                icon=ft.Icons.COPY_ROUNDED,
                                style=IconLinkStyle.DARK,
                                target=self.__copy_text,
                                tooltip="copiar número"
                            ),
                        ]
                    ),
                    # Footer
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(
                                value=self.creditcard.cardholder if self.creditcard.cardholder else "Titular",
                                font_family="AlbertSansL",
                                size=16,
                                color=tertiaryTextColor
                            ),
                            ft.Text(
                                value=self.creditcard.valid_until.strftime("%m/%y"),
                                font_family="IcelandR",
                                size=18,
                                color=tertiaryTextColor
                            ),
                        ]
                    ),
                ]
            )
        )
        self.back_content = ft.Container(
            padding=ft.padding.symmetric(vertical=24, horizontal=0),
            content=ft.Column(
                spacing=0,
                controls=[
                    ft.Container(
                        height=42,
                        bgcolor=primaryCorporate100 if not self.creditcard.expired else neutralDangerDark
                    ),
                    ft.Container(
                        height=40,
                        margin=ft.margin.symmetric(vertical=15, horizontal=24),
                        padding=ft.padding.symmetric(horizontal=8),
                        bgcolor=neutral00,
                        border_radius=4,
                        border=ft.border.all(width=1, color=neutral20),
                        content=self.card_cvc,
                        alignment=ft.alignment.center_right,
                        on_hover=self.__show_cvc,
                    ),
                ]
            )
        )

        # Widget main content
        self.content = ft.Container(
            on_click=self.__flip_card,
            on_hover=self.__scale_widget,
            content=self.front_content
        )

    def __update_face(self) -> None:
        match self.style:
            case CreditCardStyle.FRONT:
                self.content.content = self.front_content

            case CreditCardStyle.BACK:
                self.content.content = self.back_content

    def __scale_widget(self, cursor: ft.ControlEvent) -> None:
        if cursor and self.scale == 1.05:
            self.scale = 1
        else:
            self.scale = 1.05

        self.update()

    def __flip_card(self, _: ft.ControlEvent) -> None:
        self.style = CreditCardStyle.BACK if self.style == CreditCardStyle.FRONT else CreditCardStyle.FRONT
        self.__update_face()
        self.update()

    def __show_cvc(self, cursor: ft.ControlEvent) -> None:
        if cursor and self.card_cvc.value == mask_number(decrypt_data(self.creditcard.encrypted_cvc)):
            self.card_cvc.value = decrypt_data(self.creditcard.encrypted_cvc)
        else:
            self.card_cvc.value = mask_number(decrypt_data(self.creditcard.encrypted_cvc))

        self.card_cvc.update()

    def __copy_text(self, cursor: ft.ControlEvent) -> None:
        self.page.set_clipboard(decrypt_data(self.creditcard.encrypted_number))
        cursor.control.show_badge()

    def __open_edit_creditcard_form(self, _: ft.ControlEvent) -> None:
        self.page.open(
            CreditCardForm(
                title=f"Editando {self.creditcard.alias}",
                page=self.page,
                style=FormStyle.EDIT,
                creditcard=self.creditcard,
                update_changes=self.update_appearance
            )
        )

    def __open_delete_form(self, _: ft.ControlEvent) -> None:
        self.page.open(
            DeleteForm(
                page=self.page,
                item=self.creditcard,
                style=DeleteFormStyle.CREDITCARD,
                update_changes=self.update_appearance
            )
        )
