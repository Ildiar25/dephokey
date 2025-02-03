import flet as ft
from typing import Callable
import locale
from datetime import datetime

from interface.controls import CustomElevatedButton, CustomTextField

from shared.validate import Validate
from shared.logger_setup import main_logger
from shared.utils.colors import *


class DatePicker(ft.AlertDialog):
    def __init__(self, page: ft.Page, update: Callable[[datetime], None]) -> None:
        super().__init__()

        # Set locals to spanish language
        locale.setlocale(locale.LC_ALL, "es_ES.UTF-8")

        # General attributes
        self.page = page
        self.update_date = update
        self.selected_date = datetime.now()
        self.date_input = CustomTextField(
            expand=True,
            label="Nueva fecha",
            hint_text="dd-mm-aaaa",
            error_style=ft.TextStyle(
                color=dangerTextColor
            )
        )

        # Form settings
        self.modal = True

        # Form content
        self.title = ft.Text(
            value=self.selected_date.strftime("%A, %d de %B de %Y").capitalize(),
            font_family="AlbertSansB",
            size=20
        )

        self.content = ft.Container(
            width=380,
            height=80,
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text(
                                value="Introduce una fecha válida:",
                                font_family="AlbertSansL",
                                size=16
                            )
                        ]
                    ),
                    ft.Row(
                        controls=[
                            self.date_input
                        ]
                    )
                ]
            )
        )

        self.actions = [
            CustomElevatedButton(
                name="Cancelar",
                width=84,
                foreground_color=secondaryTextColor,
                on_click=lambda _: self.page.close(self),
                border_size=-1
            ),
            CustomElevatedButton(
                name="Aceptar",
                width=84,
                foreground_color=tertiaryTextColor,
                bg_color=primaryCorporateColor,
                on_click=self.validate_date,
                border_size=-1
            )
        ]

        # Form design
        self.shape = ft.RoundedRectangleBorder(4)
        self.bgcolor = bgGeneralFormColor

    def validate_date(self, _: ft.ControlEvent) -> None:
        self.date_input.error_text = None
        self.date_input.update()

        if not Validate.is_valid_date(self.date_input.value):
            self.date_input.error_text = "¡No es un formato válido!"
            self.date_input.update()
            return

        nday, nmonth, nyear = self.date_input.value.split("-")

        try:
            nday = int(nday)
            nmonth = int(nmonth)
            nyear = int(nyear)

        except ValueError as err:
            main_logger.debug(f"El usuario ha introducido '{self.date_input.value}' en el formulario.")
            main_logger.error(f"No se ha podido castear a entero el número introducido: {err}")

        else:
            # Reset values to an empty field
            self.date_input.value = ""
            self.date_input.update()

            # Sends the new date to main function
            new_date = datetime(nyear, nmonth, nday)
            self.update_date(new_date)
            self.page.close(self)



