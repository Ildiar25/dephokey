import flet as ft
import time

from data.db_orm import session

from features.models.user import User

from interface.pages.load_page import LoadPage
from interface.controls import *

from shared.validate import Validate
from shared.logger_setup import main_logger as logger
from shared.utils.masker import mask_email, mask_password
from shared.utils.colors import *


class Signup(ft.Container):
    def __init__(self, page: ft.Page) -> None:
        super().__init__()

        # General attributes (like info elements)
        self.page = page
        self.snackbar = ft.SnackBar(
            bgcolor=bgSnackbarDangerColor,
            content=ft.Text(
                "",
                text_align=ft.TextAlign.CENTER,
                color=dangerTextColor
            )
        )

        # Signup elements
        self.name = CustomTextField(
            label="Nombre Completo",
            on_change=self.toggle_signup_button_state
        )
        self.email = CustomTextField(
            label="Correo electrónico",
            on_change=self.toggle_signup_button_state
        )
        self.password = CustomTextField(
            label="Contraseña",
            on_change=self.toggle_signup_button_state,
            password=True,
            can_reveal_password=True
        )
        self.password_repeat = CustomTextField(
            label="Repite la contraseña",
            on_change=self.toggle_signup_button_state,
            password=True
        )
        self.signup_button = CustomElevatedButton(
            "Regístrate", bg_color=bgEButtonColor, foreground_color=tertiaryTextColor,
            border_size=-1, expand=True, disabled=True, on_click=self.create_account
        )

        # Page design
        self.expand = True

        # Body content
        self.content = ft.Row(
            spacing=0,
            controls=[
                # Image deco
                ft.Container(
                    expand=True,
                    image=ft.DecorationImage("interface/assets/signup-bgimage.png", fit=ft.ImageFit.COVER),
                    content=ft.Stack(
                        alignment=ft.alignment.bottom_left,
                        controls=[
                            ft.Container(
                                width=152,
                                height=48,
                                margin=ft.margin.only(50, 0, 0, 25),
                                bgcolor=ft.Colors.WHITE
                            ),
                            ft.Column(
                                expand=True,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Container(
                                        expand=True,
                                        alignment=ft.alignment.center,
                                        gradient=ft.LinearGradient(bgGradientColor,
                                                                   begin=ft.alignment.top_center,
                                                                   end=ft.alignment.bottom_center),
                                        content=ft.Icon(ft.Icons.SUPERVISED_USER_CIRCLE_ROUNDED,
                                                        size=300, color=iconAccentFormColor)
                                    )
                                ]
                            )
                        ]
                    )
                ),

                # Signup form
                ft.Container(
                    expand=True,
                    bgcolor=bgFormColor,
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=24,
                        controls=[
                            ft.Container(
                                width=380,
                                height=400,
                                content=ft.Column(
                                    spacing=24,
                                    controls=[
                                        ft.Text(
                                            "Regístrate en Dephokey",
                                            font_family="AlbertSansB",
                                            color=accentTextColor,
                                            size=24
                                        ),
                                        ft.Column(
                                            controls=[
                                                self.name,
                                                self.email,
                                                self.password,
                                                self.password_repeat
                                            ]
                                        ),
                                        ft.Row(
                                            controls=[
                                                self.signup_button
                                            ]
                                        ),
                                    ]
                                )
                            ),
                            ft.Container(
                                width=380,
                                content=ft.Row(
                                    controls=[
                                        ft.Text("¿Ya tienes cuenta?"),
                                        ft.Container(
                                            on_hover=self.focus_link,
                                            on_click=lambda _: self.page.go("/login"),
                                            content=ft.Text(
                                                "Inicia sesión!",
                                                color=accentTextColor
                                            )
                                        )
                                    ]
                                )
                            ),
                            self.snackbar
                        ]
                    )
                )
            ]
        )

    logger.info("Creación de la página 'SIGNUP' realizada.")

    @staticmethod
    def focus_link(cursor: ft.ControlEvent) -> None:
        if cursor and cursor.control.content.color == accentTextColor:
            cursor.control.content.color = secondaryTextColor
            cursor.control.content.style = ft.TextStyle(
                decoration=ft.TextDecoration.UNDERLINE,
                decoration_color=secondaryTextColor
            )
        else:
            cursor.control.content.color = accentTextColor
            cursor.control.content.style = None

        cursor.control.update()

    def toggle_signup_button_state(self, _: ft.ControlEvent) -> None:
        if all((self.name, self.email.value, self.password.value, self.password_repeat)):
            self.signup_button.disabled = False
        else:
            self.signup_button.disabled = True
        self.signup_button.update()

    def create_account(self, _: ft.ControlEvent) -> None:

        name_input = self.name.value.title().strip()
        email_input = self.email.value.lower().strip()
        password_input = self.password.value.strip()
        repeat_input = self.password_repeat.value.strip()

        # First, check if passwords are equal
        if not password_input == repeat_input:
            self.snackbar.content.value = "¡Las contraseñas no coinciden!"
            self.snackbar.open = True
            self.snackbar.update()
        else:
            # Second, validates email & password
            if not all((Validate.is_valid_email(email_input), Validate.is_valid_password(password_input))):
                self.snackbar.content.value = ("El correo o la contraseña no son válidos.\n"
                                               "La contraseña debe tener al menos un número, una mayúscula y "
                                               "una minúscula")
                self.snackbar.open = True
                self.snackbar.update()
            else:
                # Check if user already exists
                if session.query(User).filter(User.email == email_input).first():
                    logger.warning("Creación de usuario fallida: El usuario ya existe...")
                    logger.debug(f" >>> Datos: '{mask_email(email_input)}' - '{mask_password(password_input)}'")
                    self.snackbar.content.value = "¡El correo electrónico ya existe!"
                    self.snackbar.open = True
                    self.snackbar.update()
                else:
                    # Creates new user instance
                    new_user = User(fullname=name_input, email=email_input, password=password_input)
                    logger.info("Usuario creado con éxito.")
                    logger.debug(f" >>> {new_user}")

                    # Reset fields
                    self.name.value = ""
                    self.email.value = ""
                    self.password.value = ""
                    self.password_repeat.value = ""

                    # Saves user to database
                    session.add(new_user)
                    session.commit()

                    # Notifies to the user
                    self.snackbar.content.value = f"¡Bienvenido/a {new_user.fullname}!"
                    self.snackbar.content.color = successTextColor
                    self.snackbar.bgcolor = neutralSuccessLight
                    self.snackbar.open = True
                    self.snackbar.update()

                    # Report loading page
                    self.page.overlay.append(
                        LoadPage()
                    )
                    self.page.update()

                    # Load login page
                    time.sleep(2)
                    self.page.overlay.clear()
                    self.page.go("/login")
