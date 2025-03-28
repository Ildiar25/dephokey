from collections.abc import Callable
from datetime import datetime
from types import NoneType

import flet as ft

from data.db_orm import session
from features.data_encryption.core import decrypt_data, encrypt_data
from features.models import CreditCard
from features.models.user import User
from interface.controls import CustomTextField
from interface.controls.snackbar import Snackbar, SnackbarStyle
from shared.utils.colors import primaryTextColor
from shared.validate import Validate

from .base_form import BaseForm, FormStyle


class CreditCardForm(BaseForm):
    """Creates a form to edit or create a new credit card instance."""
    def __init__(
            self,
            title: str,
            page: ft.Page,
            style: FormStyle,
            snackbar: Snackbar | None = None,
            creditcard: CreditCard | None = None,
            update_changes: Callable[[], None] = None,
            update_dropdown: Callable[[], None] | None = None
    ) -> None:
        super().__init__()

        # General attributes
        self.page = page
        self.snackbar = snackbar
        self.style = style

        # Form attributes
        self.user: User = self.page.session.get("session")
        self.creditcard = creditcard
        self.update_changes = update_changes
        self.update_dropdown = update_dropdown

        # Form fields
        self.cc_alias = CustomTextField(
            hint_text="Agrega un alias",
            on_change=self.__update_field_inputs,
            max_length=30
        )
        self.cc_holder = CustomTextField(
            hint_text="Introduce el nombre del titular",
            on_change=self.__update_field_inputs,
            max_length=30
        )
        self.cc_number = CustomTextField(
            hint_text="Añade el número de tarjeta",
            can_reveal_password=True,
            max_length=19,
            password=True,
            input_filter=ft.NumbersOnlyInputFilter(),
            on_change=self.__update_field_inputs
        )
        self.cc_cvc = CustomTextField(
            hint_text="cvc",
            width=104,
            password=True,
            can_reveal_password=True,
            max_length=4,
            on_change=self.__update_field_inputs,
            input_filter=ft.NumbersOnlyInputFilter()
        )
        self.cc_date = CustomTextField(
            hint_text="mm/yy",
            width=420,
            max_length=5,
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
            case FormStyle.ADD:
                self.submit_button.on_click = self.__add_creditcard

                # Content
                self.content.content = ft.Column(
                    spacing=14,
                    controls=[
                        ft.Column(
                            spacing=6,
                            controls=[
                                ft.Text(value="Alias", font_family="AlbertSansR", color=primaryTextColor),
                                self.cc_alias,
                            ]
                        ),
                        ft.Column(
                            spacing=6,
                            controls=[
                                ft.Text(value="Nombre del titular", font_family="AlbertSansR", color=primaryTextColor),
                                self.cc_holder,
                            ]
                        ),
                        ft.Column(
                            spacing=6,
                            controls=[
                                ft.Text(
                                    value="Número de la tarjeta",
                                    font_family="AlbertSansR",
                                    color=primaryTextColor,
                                    spans=[self.span, ]
                                ),
                                self.cc_number,
                            ]
                        ),
                        ft.Row(
                            spacing=16,
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Column(
                                    spacing=6,
                                    controls=[
                                        ft.Text(
                                            value="Fecha de validez",
                                            font_family="AlbertSansR",
                                            color=primaryTextColor,
                                            spans=[self.span, ]
                                        ),
                                        self.cc_date,
                                    ]
                                ),
                                ft.Column(
                                    spacing=6,
                                    controls=[
                                        ft.Text(
                                            value="CVC",
                                            font_family="AlbertSansR",
                                            color=primaryTextColor,
                                            spans=[self.span, ]
                                        ),
                                        self.cc_cvc,
                                    ]
                                ),
                            ]
                        ),
                    ]
                )

            case FormStyle.EDIT:
                self.submit_button.on_click = self.__update_creditcard
                self.cc_alias.value = self.creditcard.alias
                self.cc_holder.value = self.creditcard.cardholder
                self.cc_number.value = decrypt_data(self.creditcard.encrypted_number)
                self.cc_date.value = self.creditcard.valid_until.strftime("%m/%y")
                self.cc_cvc.value = decrypt_data(self.creditcard.encrypted_cvc)

                # Content
                self.content.content = ft.Column(
                    spacing=14,
                    controls=[
                        ft.Column(
                            spacing=6,
                            controls=[
                                ft.Text(value="Alias", font_family="AlbertSansR", color=primaryTextColor),
                                self.cc_alias,
                            ]
                        ),
                        ft.Column(
                            spacing=6,
                            controls=[
                                ft.Text(value="Nombre del titular", font_family="AlbertSansR", color=primaryTextColor),
                                self.cc_holder,
                            ]
                        ),
                        ft.Column(
                            spacing=6,
                            controls=[
                                ft.Text(
                                    value="Número de la tarjeta",
                                    font_family="AlbertSansR",
                                    color=primaryTextColor,
                                    spans=[self.span, ]
                                ),
                                self.cc_number,
                            ]
                        ),
                        ft.Row(
                            spacing=16,
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Column(
                                    spacing=6,
                                    controls=[
                                        ft.Text(
                                            value="Fecha de validez",
                                            font_family="AlbertSansR",
                                            color=primaryTextColor,
                                            spans=[self.span, ]
                                        ),
                                        self.cc_date,
                                    ]
                                ),
                                ft.Column(
                                    spacing=6,
                                    controls=[
                                        ft.Text(
                                            value="CVC",
                                            font_family="AlbertSansR",
                                            color=primaryTextColor,
                                            spans=[self.span, ]
                                        ),
                                        self.cc_cvc,
                                    ]
                                ),
                            ]
                        ),
                    ]
                )

    def __update_field_inputs(self, cursor: ft.ControlEvent) -> None:
        self.cc_number.reset_error()
        self.cc_date.reset_error()
        self.fields = [self.cc_number.value, self.cc_date.value, self.cc_cvc.value]
        self._toggle_submit_button_state(cursor)

    def __add_creditcard(self, _: ft.ControlEvent) -> None:
        nw_alias = self.cc_alias.value.capitalize().strip() if self.cc_alias.value else "Alias tarjeta"
        nw_cardholder = self.cc_holder.value.title().strip() if self.cc_holder.value else self.user.fullname
        nw_number = self.cc_number.value.strip()
        nw_date = self.cc_date.value.strip()
        nw_cvc = self.cc_cvc.value.strip()

        if not Validate.is_valid_creditcard_number(nw_number):
            self.cc_number.show_error("Introduce un número de tarjeta válido.")
            return

        if not Validate.is_valid_date(nw_date):
            self.cc_date.show_error("No es una fecha válida.")
            return

        # Create new creditcard-instance
        nw_date = datetime.strptime(nw_date, "%m/%y")
        new_creditcard = CreditCard(nw_cardholder, nw_number, nw_cvc, nw_date, self.user, nw_alias)
        self.__save_changes(new_creditcard)

        self.__display_message(msg=f"¡'{nw_alias}' añadida!", style=SnackbarStyle.SUCCESS)
        self.page.close(self)

    def __update_creditcard(self, _: ft.ControlEvent) -> None:
        new_alias = self.cc_alias.value.capitalize().strip() if self.cc_alias.value else "Alias tarjeta"
        new_holder = self.cc_holder.value.title().strip() if self.cc_holder.value else self.user.fullname
        new_number = self.cc_number.value.strip()
        new_date = self.cc_date.value.strip()
        new_cvc = self.cc_cvc.value.strip()

        if not Validate.is_valid_creditcard_number(new_number):
            self.cc_number.show_error("Introduce un número de tarjeta válido.")
            return

        if not Validate.is_valid_date(new_date):
            self.cc_date.show_error("No es una fecha válida.")
            return

        # Update creditcard-data
        self.__update_data(new_alias, new_cvc, new_date, new_holder, new_number)

        self.__save_changes()
        self.page.close(self)

    def __save_changes(self, creditcard: CreditCard | None = None) -> None:
        if creditcard is not None:
            session.add(creditcard)

        session.commit()

        self.update_changes()
        if not isinstance(self.update_dropdown, NoneType):
            self.update_dropdown()

    def __update_data(self, alias, cvc, date, cardholder, number):
        self.creditcard.alias = alias
        self.creditcard.cardholder = cardholder
        self.creditcard.encrypted_number = encrypt_data(number)
        self.creditcard.valid_until = datetime.strptime(date, "%m/%y")
        self.creditcard.encrypted_cvc = encrypt_data(cvc)
        self.creditcard.update_expired()

    def __display_message(self, msg: str, style: SnackbarStyle) -> None:
        self.snackbar.change_style(msg=msg, style=style)
        self.snackbar.update()
