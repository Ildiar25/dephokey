import flet as ft
import random
from hashlib import sha256
from string import ascii_letters, digits

from data.db_orm import session

from features.models.user import User

from .base_form import BaseForm, FormStyle
from interface.controls import Snackbar, SnackbarStyle, CustomTextField, TextLink

from shared.validate import Validate
from shared.utils.colors import *


class ChangePasswordForm(BaseForm):
    def __init__(self, page: ft.Page, snackbar: Snackbar, style: FormStyle, email: str | None = None) -> None:
        super().__init__()

        # General attributes
        self.page = page
        self.snackbar = snackbar
        self.style = style

        # Form attributes
        self.email = email

        # Form fields
        self.main_pw = CustomTextField(password=True, can_reveal_password=True, max_length=50,
            on_change=self.__update_field_inputs
        )
        self.auxiliar_pw = CustomTextField(password=True, can_reveal_password=True, max_length=50,
            on_change=self.__update_field_inputs
        )

        # Form settings
        self.cancel_button.on_click = lambda _: self.page.close(self)

        # Form title
        self.title = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text(value="Cambiar contraseña", font_family="AlbertSansB", size=20, color=primaryTextColor),
                self.close_button
            ]
        )

        self.__update_appearance()

    def __update_appearance(self) -> None:
        match self.style:
            case FormStyle.EDIT:
                self.user: User = self.page.session.get("session")
                self.submit_button.on_click = self.__update_password

                # Content
                self.content.content = ft.Column(alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Row(wrap=True,
                            controls=[
                                ft.Text(value="¡Atención! ", color=primaryTextColor, font_family="AlbertSansB",
                                    spans=[
                                        ft.TextSpan(
                                            text="Si olvidas la contraseña deberás restaurarla desde el principio."
                                                 " Por tu seguridad, ",
                                            style=ft.TextStyle(font_family="AlbertSansL")),
                                        ft.TextSpan(
                                            text="las contraseñas no se almacenan en la base de datos, ",
                                            style=ft.TextStyle(font_family="AlbertSansB")),
                                        ft.TextSpan(
                                            text="por lo que ",
                                            style=ft.TextStyle(font_family="AlbertSansL")),
                                        ft.TextSpan(
                                            text="es importante que la recuerdes.\n\n",
                                            style=ft.TextStyle(font_family="AlbertSansB")),
                                        ft.TextSpan(
                                            text="Puedes introducir tu nueva contraseña de forma manual o generarla "
                                                 "automáticamente desde el botón ",
                                            style=ft.TextStyle(font_family="AlbertSansL")),
                                        ft.TextSpan(
                                            text="Generar Contraseña. ",
                                            style=ft.TextStyle(font_family="AlbertSansI")),
                                        ft.TextSpan(
                                            text="Aunque te recomendamos que utilices la tuya propia.",
                                            style=ft.TextStyle(font_family="AlbertSansL")),
                                    ])
                            ]
                        ),
                        ft.Row(
                            controls=[
                                ft.Column(spacing=8, expand=True,
                                    controls=[
                                        ft.Text(value="Contraseña", font_family="AlbertSansR", color=primaryTextColor,
                                                spans=[self.span]),
                                        self.main_pw,
                                        ft.Text(value="Repite la contraseña", font_family="AlbertSansR",
                                                color=primaryTextColor, spans=[self.span]),
                                        self.auxiliar_pw
                                    ]
                                )
                            ]
                        ),
                        ft.Row(
                            controls=[
                                TextLink(text="Generar Contraseña", function=self.__generate_password)
                            ]
                        )
                    ]
                )

            case FormStyle.RESET:
                self.submit_button.on_click = self.__reset_password

                # Content
                self.content.content = ft.Column(alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Row(wrap=True,
                            controls=[
                                ft.Text(value="¡Atención!", color=primaryTextColor, font_family="AlbertSansB",
                                    spans=[
                                        ft.TextSpan(
                                            text=f" Estas cambiando la contraseña de la cuenta ",
                                            style=ft.TextStyle(font_family="AlbertSansL")),
                                        ft.TextSpan(
                                            text=f"{repr(self.email)}. ",
                                            style=ft.TextStyle(font_family="AlbertSansB")),
                                        ft.TextSpan(
                                            text="Por tu seguridad, ",
                                            style=ft.TextStyle(font_family="AlbertSansL")),
                                        ft.TextSpan(
                                            text="las contraseñas no se almacenan en la base de datos, ",
                                            style=ft.TextStyle(font_family="AlbertSansB")),
                                        ft.TextSpan(
                                            text="por lo que ",
                                            style=ft.TextStyle(font_family="AlbertSansL")),
                                        ft.TextSpan(
                                            text="es importante que la recuerdes.\n\n",
                                            style=ft.TextStyle(font_family="AlbertSansB")),
                                        ft.TextSpan(
                                            text="Puedes introducir tu nueva contraseña de forma manual o generarla "
                                                 "automáticamente desde el botón ",
                                            style=ft.TextStyle(font_family="AlbertSansL")),
                                        ft.TextSpan(
                                            text="Generar Contraseña. ",
                                            style=ft.TextStyle(font_family="AlbertSansI")),
                                        ft.TextSpan(
                                            text="Aunque te recomendamos que utilices la tuya propia.",
                                            style=ft.TextStyle(font_family="AlbertSansL")),
                                    ])
                            ]
                        ),
                        ft.Row(
                            controls=[
                                ft.Column(spacing=8, expand=True,
                                    controls=[
                                        ft.Text(value="Contraseña", font_family="AlbertSansR", color=primaryTextColor,
                                                spans=[self.span]),
                                        self.main_pw,
                                        ft.Text(value="Repite la contraseña", font_family="AlbertSansR",
                                                color=primaryTextColor, spans=[self.span]),
                                        self.auxiliar_pw
                                    ]
                                )
                            ]
                        ),
                        ft.Row(
                            controls=[
                                TextLink(text="Generar Contraseña", function=self.__generate_password)
                            ]
                        )
                    ]
                )

    def __update_field_inputs(self, cursor:ft.ControlEvent) -> None:
        self.main_pw.reset_error()
        self.auxiliar_pw.reset_error()
        self.fields = [self.main_pw, self.auxiliar_pw]
        self.toggle_submit_button_state(cursor)

    def __generate_password(self, _: ft.ControlEvent) -> None:
        dictionary = ascii_letters + digits
        secure_password = ""

        while len(secure_password) < 15:
            secure_password += random.choice(dictionary)

        self.main_pw.value = secure_password
        self.main_pw.update()

    def __update_password(self, _: ft.ControlEvent) -> None:
        new_password = self.main_pw.value.strip()
        pass_checking = self.auxiliar_pw.value.strip()

        if not new_password == pass_checking:
            self.main_pw.reset_error()
            self.auxiliar_pw.show_error("Las contraseñas no coinciden.")
            return

        if not Validate.is_valid_password(new_password):
            self.auxiliar_pw.reset_error()
            self.main_pw.show_error("Contraseña inválida: debe contener mínimo mayúsculas, minúsculas y un número.")
            return

        self.main_pw.reset_error()
        self.auxiliar_pw.reset_error()

        self.user.hashed_password = sha256(new_password.encode()).hexdigest()
        session.commit()

        self.snackbar.change_style(msg="¡Contraseña actualizada!", style=SnackbarStyle.SUCCESS)
        self.snackbar.update()
        self.page.close(self)

    def __reset_password(self, _:ft.ControlEvent) -> None:
        self.user = session.query(User).filter_by(email=self.email).first()
        new_password = self.main_pw.value.strip()
        pass_checking = self.auxiliar_pw.value.strip()

        if not new_password == pass_checking:
            self.main_pw.reset_error()
            self.auxiliar_pw.show_error("Las contraseñas no coinciden.")
            return

        if not Validate.is_valid_password(new_password):
            self.auxiliar_pw.reset_error()
            self.main_pw.show_error("Contraseña inválida: debe contener mínimo mayúsculas, minúsculas y un número.")
            return

        self.main_pw.reset_error()
        self.auxiliar_pw.reset_error()

        self.user.hashed_password = sha256(new_password.encode()).hexdigest()
        session.commit()

        self.snackbar.change_style(msg="¡Contraseña actualizada!", style=SnackbarStyle.SUCCESS)
        self.snackbar.update()
        self.page.close(self)
