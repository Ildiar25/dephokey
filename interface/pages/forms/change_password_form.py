import flet as ft
import random
from string import ascii_lowercase, ascii_uppercase, digits
from hashlib import sha256

from data.db_orm import session

from features.models.user import User

from interface.controls import CustomElevatedButton, CustomTextField

from shared.validate import Validate
from shared.utils.colors import *


class ChangePasswordForm(ft.AlertDialog):
    def __init__(self, page: ft.Page) -> None:
        super().__init__()

        # General attributes
        self.page = page
        self.submit_button = CustomElevatedButton(
            name="Aceptar", width=100, bg_color=bgEButtonColor, foreground_color=tertiaryTextColor,
            on_click=self.update_password, border_size=-1, disabled=True
        )
        self.generate_password = CustomElevatedButton(
            name="Generar", width=84, foreground_color=tertiaryTextColor, bg_color=neutralDangerMedium,
            on_click=self.generate_password, border_size=-1
        )
        self.password = CustomTextField(
            expand=True, on_change=self.toggle_generate_button_state,
            password=True, can_reveal_password=True

        )
        self.check_password = CustomTextField(
            expand=True, on_change=self.toggle_generate_button_state,
            password=True, can_reveal_password=True

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
            width=530,
            height=248,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Column(
                                width=80,
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, size=40, color=neutralWarningMedium)
                                ]
                            ),
                            ft.Row(
                                expand=True,
                                wrap=True,
                                controls=[
                                    ft.Text(
                                        "Atención: Si olvida la contraseña deberá volver a restaurarla desde el "
                                        "principio. Por su seguridad las contraseñas no se almacenan en la "
                                        "base de datos y no vamos a explicar ahora cómo lo hacen...",
                                        color=secondaryTextColor
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
                                        "Contraseña:",
                                        font_family="AlbertSansR",
                                        size=16,
                                        color=primaryTextColor
                                    ),
                                    ft.Row(controls=[self.password]),
                                    ft.Text(
                                        "Repite la contraseña:",
                                        font_family="AlbertSansR",
                                        size=16,
                                        color=primaryTextColor
                                    ),
                                    ft.Row(controls=[self.check_password])
                                ]
                            )
                        ]
                    )
                ]
            )
        )

        # F-Buttons
        self.actions = [self.generate_password, self.submit_button]

        # Form design
        self.shape = ft.RoundedRectangleBorder(4)
        self.bgcolor = bgGeneralFormColor

    def toggle_generate_button_state(self, cursor: ft.ControlEvent) -> None:
        if cursor and all((self.password.value, self.check_password.value)):
            self.submit_button.disabled = False
        else:
            self.submit_button.disabled = True
        self.submit_button.update()



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
            self.password.error_text = ""
            self.password.update()
            self.check_password.error_text = "Las contraseñas no coinciden"
            self.check_password.update()

        else:
            # Second, validates password
            if not Validate.is_valid_password(password):
                self.check_password.error_text = ""
                self.check_password.update()
                self.password.error_text = "La contraseña no es válida"
                self.password.update()

            else:
                self.password.error_text = ""
                self.password.update()
                self.check_password.error_text = ""
                self.check_password.update()

                # Loads user & change Hash
                user: User = self.page.session.get("session")
                user.hashed_password = sha256(password.encode()).hexdigest()

                # Save changes
                session.commit()

                self.page.close(self)
