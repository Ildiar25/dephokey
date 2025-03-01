from string import ascii_lowercase, ascii_uppercase, digits, punctuation
from faker import Faker
import flet as ft
import random

from .base_form import BaseForm, FormStyle
from interface.controls import CustomElevatedButton, ButtonStyle, CustomSwitch, CustomTextField, IconLink, IconLinkStyle

from shared.logger_setup import main_log as log
from shared.utils.colors import *


class GenerateForm(BaseForm):
    def __init__(self, title: str, page: ft.Page, style: FormStyle) -> None:
        super().__init__()

        # General attributes
        self.page = page
        self.style = style

        # Form attributes
        self.result = CustomTextField(read_only=True, expand=True)

        # Form settings
        self.submit_button = CustomElevatedButton(name="Generar", style=ButtonStyle.DEFAULT)
        self.cancel_button.on_click = lambda _: self.page.close(self)

        # Form title
        self.title = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text(title, font_family="AlbertSansB", size=20, color=primaryTextColor), self.close_button
            ]
        )

        self.actions = [self.cancel_button, self.submit_button]

        self.__update_appearance()

    def __update_appearance(self):
        match self.style:
            case FormStyle.PASSWORD:
                self.submit_button.on_click = self.__generate_password
                self.number_input = CustomTextField(width=76, max_length=2, input_filter=ft.NumbersOnlyInputFilter())
                self.fields = [
                    CustomSwitch(title="Minúsculas", width=240, on_change=self.toggle_submit_button_state, value=True),
                    CustomSwitch(title="Mayúsculas", width=240, on_change=self.toggle_submit_button_state),
                    CustomSwitch(title="Números", width=240, on_change=self.toggle_submit_button_state),
                    CustomSwitch(title="Caracteres especiales", width=240, on_change=self.toggle_submit_button_state),
                ]

                # Content
                self.content.content = ft.Column(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, spacing=22,
                    controls=[
                        ft.Row(wrap=True,
                            controls=[
                                ft.Text(
                                    value="Indica las características que necesita tu contraseña. Puedes generarla "
                                          "más de una vez si no estás conforme con el resultado:",
                                    font_family="AlbertSansR", color=primaryTextColor, size=16
                                )
                            ]
                        ),
                        ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Column(horizontal_alignment=ft.CrossAxisAlignment.END,
                                    controls=[self.fields[0], self.fields[1]]
                                ),
                                ft.Column(horizontal_alignment=ft.CrossAxisAlignment.END,
                                    controls=[self.fields[2], self.fields[3]]
                                )
                            ]
                        ),
                        ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text(
                                    value="Número máximo de caracteres:",
                                    font_family="AlbertSansB", color=primaryTextColor, spans=[
                                        ft.TextSpan(text="\nEl número por defecto es de 12 caracteres y\npuedes "
                                            "colocar un máximo de 99.", style=ft.TextStyle(font_family="AlbertSansL"))
                                    ]
                                ),
                                self.number_input
                            ]
                        ),
                        ft.Row(
                            controls=[
                                self.result,
                                IconLink(ft.Icons.COPY_ROUNDED, style=IconLinkStyle.LIGHT,
                                    function=self.copy_text, tooltip="copiar contraseña")
                            ]
                        )
                    ]
                )

            case FormStyle.CC_NUMBER:
                self.content = ft.Container(width=524, height=150)
                self.submit_button.on_click = self.__generate_number

                # Content
                self.content.content = ft.Column(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, spacing=22,
                    controls=[
                        ft.Row(wrap=True,
                            controls=[
                                ft.Text(
                                    value="Al darle al botón, se generará un número de tarjeta válido para poder "
                                          "almacenarlo en la base de datos.",
                                    font_family="AlbertSansR", color=primaryTextColor, size=16
                                )
                            ]
                        ),
                        ft.Row(
                            controls=[
                                self.result,
                                IconLink(ft.Icons.COPY_ROUNDED, style=IconLinkStyle.LIGHT,
                                    function=self.copy_text, tooltip="copiar contraseña")
                            ]
                        )
                    ]
                )

    def __generate_password(self, _: ft.ControlEvent) -> None:
        password_length = 12
        dictionary = self.__update_dictionary()
        new_password = ""

        if self.number_input.value:
            try:
                password_length = int(self.number_input.value)

            except ValueError as text_number:
                password_length = 12
                log.error(f"'{self.number_input.value}' no es un número válido.", text_number)

        while len(new_password) < password_length:
            new_password += random.choice(dictionary)

        self.result.value = new_password
        self.result.update()

    def __update_dictionary(self) -> str:
        dictionary = ""

        if self.fields[0].get_value(): dictionary += ascii_lowercase
        if self.fields[1].get_value(): dictionary += ascii_uppercase
        if self.fields[2].get_value(): dictionary += digits
        if self.fields[3].get_value(): dictionary += punctuation

        return dictionary.replace(" ", "")

    def __generate_number(self, _: ft.ControlEvent) -> None:
        # Initialize faker class
        faker = Faker('es_ES')

        # Create new creditcard number
        self.result.value = faker.credit_card_number()
        self.result.update()

    def copy_text(self, cursor: ft.ControlEvent) -> None:
        self.page.set_clipboard(self.result.value)
        cursor.control.show_badge()

    def toggle_submit_button_state(self, cursor: ft.ControlEvent) -> None:
        if cursor and any((filter(lambda switch: switch.get_value(), self.fields))):  # Gets bool value from each switch
            self.submit_button.disabled = False
        else:
            self.submit_button.disabled = True
        self.submit_button.update()
