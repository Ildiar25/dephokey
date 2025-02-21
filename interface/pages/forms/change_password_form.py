from string import ascii_lowercase, ascii_uppercase, digits
import flet as ft
import random
from hashlib import sha256

from data.db_orm import session

from features.models.user import User

from interface.controls import CustomElevatedButton, ButtonStyle, CustomTextField, Snackbar, SnackbarStyle, TextLink

from shared.validate import Validate
from shared.utils.colors import *


class ChangePasswordForm(ft.AlertDialog):
    def __init__(self, page: ft.Page, snackbar: Snackbar) -> None:
        super().__init__()

        # General attributes
        self.page = page
        self.snackbar = snackbar

        # TODO: Tener en cuenta que puede o no puede haber usuario. Es el mismo formulario para cuando se necesite un
        #  reseteo de contraseña. Implementar dicho flujo de trabajo.

        # Form attributes
        self.user: User = self.page.session.get("session")
        self.submit = CustomElevatedButton(
            name="Aceptar", style=ButtonStyle.DEFAULT, on_click=self.update_password, disabled=True
        )
        self.password = CustomTextField(
            expand=True, on_change=self.toggle_generate_button_state, password=True, can_reveal_password=True
        )
        self.check_password = CustomTextField(
            expand=True, on_change=self.toggle_generate_button_state, password=True, can_reveal_password=True
        )

        # Form settings
        self.modal = True

        # F-Title
        self.title = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text(
                    value="Cambiar Contraseña",
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
        self.content = ft.Container(
            width=550,
            height=378,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Row(
                                expand=True,
                                wrap=True,
                                controls=[
                                    ft.Text(
                                        value="¡Atención!",
                                        color=primaryTextColor,
                                        spans=[
                                            ft.TextSpan(text=" Si olvidas la contraseña deberás restaurarla desde el "
                                                        "principio. Por tu seguridad,",
                                                        style=ft.TextStyle(font_family="AlbertSansL")),
                                            ft.TextSpan(text=" las contraseñas no se almacenan en la base de datos,",
                                                        style=ft.TextStyle(font_family="AlbertSansB")),
                                            ft.TextSpan(text=" por lo que",
                                                        style=ft.TextStyle(font_family="AlbertSansL")),
                                            ft.TextSpan(text=" es importante que la recuerdes.\n\n",
                                                        style=ft.TextStyle(font_family="AlbertSansB")),
                                            ft.TextSpan(text="Puedes introducir tu nueva contraseña de forma manual o "
                                                        "generarla automáticamente desde el botón",
                                                        style=ft.TextStyle(font_family="AlbertSansL")),
                                            ft.TextSpan(text=" Generar Contraseña.",
                                                        style=ft.TextStyle(font_family="AlbertSansI"))
                                        ],
                                        font_family="AlbertSansB"
                                    )
                                ]
                            )
                        ]
                    ),
                    ft.Row(
                        controls=[
                            ft.Column(
                                expand=True,
                                spacing=8,
                                controls=[
                                    ft.Text(
                                        value="Contraseña:",
                                        font_family="AlbertSansR",
                                        size=16,
                                        color=primaryTextColor
                                    ),
                                    ft.Row(controls=[self.password]),
                                    ft.Text(
                                        value="Repite la contraseña:",
                                        font_family="AlbertSansR",
                                        size=16,
                                        color=primaryTextColor
                                    ),
                                    ft.Row(controls=[self.check_password])
                                ]
                            )
                        ]
                    ),
                    ft.Row(
                        controls=[
                            TextLink(text="Generar contraseña", function=self.generate_password)
                        ]
                    )
                ]
            )
        )

        # F-Buttons
        self.actions = [
            CustomElevatedButton(
                name="Cancelar", style=ButtonStyle.CANCEL, on_click=lambda _: self.page.close(self)
            ),
            self.submit
        ]

        # Form design
        self.shape = ft.RoundedRectangleBorder(4)
        self.bgcolor = bgGeneralFormColor

    def toggle_generate_button_state(self, cursor: ft.ControlEvent) -> None:
        if cursor and all((self.password.value, self.check_password.value)):
            self.submit.disabled = False
        else:
            self.submit.disabled = True
        self.submit.update()

    def generate_password(self, _: ft.ControlEvent) -> None:
        characters = ascii_lowercase + digits + ascii_uppercase
        new_password = ""

        while len(new_password) < 12:
            new_password += random.choice(characters)

        self.password.value = new_password
        self.password.update()

    def update_password(self, _: ft.ControlEvent) -> None:

        password = self.password.value.strip()
        check_password = self.check_password.value.strip()

        # First, check if passwords are equal
        if not password == check_password:
            self.password.reset_error()
            self.check_password.show_error("Las contraseñas no coinciden")

        else:
            # Second, validates password
            if not Validate.is_valid_password(password):
                self.check_password.reset_error()
                self.password.show_error(
                    "Contraseña inválida: debe contener mínimo mayúsculas, minúsculas y un número."
                )

            else:
                self.password.reset_error()
                self.check_password.reset_error()

                # Loads user & change Hash
                self.user.hashed_password = sha256(password.encode()).hexdigest()

                # Save changes
                session.commit()

                self.snackbar.change_style(msg="¡Contraseña actualizada!", style=SnackbarStyle.SUCCESS)
                self.snackbar.update()
                self.page.close(self)
