import flet as ft
from enum import Enum
from string import ascii_lowercase, ascii_uppercase, digits, punctuation
from faker import Faker
import random
import time

from interface.controls import CustomElevatedButton, CustomSwitch, CustomTextField

from shared.utils.colors import *


class GenerateFormStyle(Enum):
    PASSWORD = "password"
    NUMBER = "number"


class GenerateForm(ft.AlertDialog):
    def __init__(self, page: ft.Page, title: str, generate_style: GenerateFormStyle) -> None:
        super().__init__()

        # General attributes
        self.page = page
        self.generate_style = generate_style
        self.submit_button = CustomElevatedButton(
            name="Generar", bg_color=bgEButtonColor, foreground_color=tertiaryTextColor,
            border_size=-1, expand=True, disabled=False
        )
        self.result = CustomTextField(expand=True, read_only=True)
        self.copybutton = ft.IconButton(
            ft.Icons.COPY_ROUNDED,
            icon_color=primaryCorporateColor,
            on_click=self.copy_text,
            highlight_color=selectedIconGeneralFormColor,
            hover_color=hoverIconGeneralFormColor,
            tooltip="Copiar al portapapeles"
        )

        # Content according to style
        match generate_style:
            case GenerateFormStyle.PASSWORD:

                # GeneratePassword attributes
                self.switches = [
                    CustomSwitch(title="Minúsculas", width=240, on_change=self.toggle_generate_button_state,
                                 value=True),
                    CustomSwitch(title="Mayúsculas", width=240, on_change=self.toggle_generate_button_state),
                    CustomSwitch(title="Números", width=240, on_change=self.toggle_generate_button_state),
                    CustomSwitch(title="Caracteres Especiales", width=240, on_change=self.toggle_generate_button_state)
                ]
                self.max_input = CustomTextField(width=76, max_length=3, on_change=self.change_number_input)
                self.submit_button.on_click = self.generate_password
                self.bodycontent = ft.Container(
                    width=524,
                    height=300,
                    content=ft.Column(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        spacing=22,
                        controls=[
                            ft.Row(
                                wrap=True,
                                controls=[
                                    ft.Text(
                                        value="Indica las características que necesita tu contraseña. Puedes "
                                              "generarla más de una vez si no estás conforme con el resultado:",
                                        font_family="AlbertSansR",
                                        size=16,
                                        color=primaryTextColor
                                    )
                                ]
                            ),
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Column(
                                        horizontal_alignment=ft.CrossAxisAlignment.END,
                                        controls=[
                                            self.switches[0],
                                            self.switches[1]
                                        ]
                                    ),
                                    ft.Column(
                                        horizontal_alignment=ft.CrossAxisAlignment.END,
                                        controls=[
                                            self.switches[2],
                                            self.switches[3]
                                        ]
                                    )
                                ]
                            ),
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text(value="Número máximo de caracteres:\n"
                                                  "El número mínimo es de 7 caracteres y un máximo de 50.",
                                            font_family="AlbertSansL",
                                            color=primaryTextColor),
                                    self.max_input
                                ]
                            ),
                            ft.Row(
                                controls=[
                                    self.result, self.copybutton
                                ]
                            )
                        ]
                    )
                )

            case GenerateFormStyle.NUMBER:
                self.submit_button.on_click = self.generate_cardnumber
                self.bodycontent = ft.Container(
                    width=524,
                    height=150,
                    content=ft.Column(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        spacing=22,
                        controls=[
                            ft.Row(
                              controls=[
                                  ft.Text(value="Al darle al botón, se generará un número de tarjeta\n"
                                                "válido para poder almacenarlo en la base de datos.",
                                          font_family="AlbertSansL",
                                          color=primaryTextColor)
                              ]
                            ),
                            ft.Row(
                                controls=[
                                    self.result, self.copybutton
                                ]
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
        self.actions = [self.submit_button]

        # Form design
        self.shape = ft.RoundedRectangleBorder(4)
        self.bgcolor = bgGeneralFormColor

    def copy_text(self, cursor: ft.ControlEvent) -> None:
        self.page.set_clipboard(self.result.value)
        cursor.control.badge = ft.Badge(
            text="Copiado!",
            bgcolor=ft.Colors.with_opacity(opacity=0.5, color=neutral80),
            text_color=neutral05
        )
        cursor.control.update()
        time.sleep(1)
        cursor.control.badge.label_visible = False
        cursor.control.update()

    def toggle_generate_button_state(self, _: ft.ControlEvent) -> None:
        if any((filter(lambda button: button.get_value(), self.switches))):
            self.submit_button.disabled = False
        else:
            self.submit_button.disabled = True
        self.submit_button.update()

    def change_number_input(self, _: ft.ControlEvent) -> None:
        if not self.max_input.value.isdigit():
            self.max_input.value = ""
            self.max_input.update()
            return

        num = int(self.max_input.value)
        if num > 50:
            self.max_input.value = "50"
            self.max_input.update()

    def generate_cardnumber(self, _: ft.ControlEvent) -> None:
        # Initializes the class Faker
        fake = Faker()

        # Creates a new credit card number
        new_creditcard_number = fake.credit_card_number()

        # Updates value
        self.result.value = new_creditcard_number
        self.result.update()

    def generate_password(self, _: ft.ControlEvent):
        try:
            if not self.max_input.value:
                max_value = 7

            else:
                max_value = 7 if int(self.max_input.value) < 7 else int(self.max_input.value)

        except ValueError as err:
            print("OPS!", err)

        else:
            text_dict = ""

            if self.switches[0].get_value():
                text_dict += ascii_lowercase
            if self.switches[1].get_value():
                text_dict += ascii_uppercase
            if self.switches[2].get_value():
                text_dict += digits
            if self.switches[3].get_value():
                text_dict += punctuation

            self.result.value = self.create_password(max_len=max_value, characters=text_dict)
            self.result.update()

    @staticmethod
    def create_password(max_len: int, characters: str) -> str:
        new_password = ""

        while len(new_password) < max_len:
            new_password += random.choice(characters)

        return new_password
