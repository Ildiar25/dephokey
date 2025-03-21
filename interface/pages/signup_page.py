import time

import flet as ft

from data.db_orm import session
from features.models.user import User
from interface.controls import CustomElevatedButton, CustomTextField, TextLink
from interface.controls.e_button import ButtonStyle
from interface.controls.snackbar import Snackbar, SnackbarStyle
from interface.pages.loading_page import LoadingPage
from shared.logger_setup import main_log as log
from shared.utils.colors import accentTextColor, neutral00
from shared.utils.masker import mask_email, mask_password
from shared.validate import Validate


class Signup(ft.Container):
    """Creates Signup page and displays all form elements"""
    def __init__(self, page: ft.Page) -> None:
        super().__init__()

        # Page attributes
        self.page = page
        self.snackbar = Snackbar()

        # Signup attributes
        self.name = CustomTextField(
            label="Nombre Completo",
            on_change=self.__toggle_signup_button_state,
            autofocus=True,
            max_length=150
        )
        self.email = CustomTextField(
            label="Correo electrónico",
            on_change=self.__toggle_signup_button_state,
            max_length=50
        )
        self.password = CustomTextField(
            label="Contraseña",
            on_change=self.__toggle_signup_button_state,
            password=True,
            can_reveal_password=True,
            max_length=50
        )
        self.password_repeat = CustomTextField(
            label="Repite la contraseña",
            on_change=self.__toggle_signup_button_state,
            on_submit=self.__create_account,
            password=True,
            can_reveal_password=True,
            max_length=50
        )
        self.signup_button = CustomElevatedButton(
            name="Regístrate",
            style=ButtonStyle.DEFAULT,
            expand=True,
            disabled=True,
            on_click=self.__create_account
        )

        # Page design
        self.expand = True

        # Body content
        self.content = ft.Row(
            spacing=0,
            controls=[
                # Lateral decoration
                ft.Container(
                    expand=True,
                    image=ft.DecorationImage("interface/assets/bg-image-signup.png", fit=ft.ImageFit.COVER),
                    content=ft.Stack(
                        alignment=ft.alignment.top_left,
                        controls=[
                            ft.Container(
                                width=152,
                                height=48,
                                margin=ft.margin.only(left=50, top=25),
                                content=ft.Image("interface/assets/logotype-white.svg")
                            ),
                            ft.Column(
                                expand=True,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Container(
                                        expand=True,
                                        alignment=ft.alignment.center,
                                        content=ft.Image(src="interface/assets/signup-passkey.svg", width=350)
                                    ),
                                ]
                            ),
                        ]
                    )
                ),

                # Signup form
                ft.Container(
                    expand=True,
                    bgcolor=neutral00,
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
                                            value="Regístrate en Dephokey",
                                            font_family="AlbertSansB",
                                            color=accentTextColor,
                                            size=24
                                        ),
                                        ft.Column(
                                            controls=[
                                                self.name,
                                                self.email,
                                                self.password,
                                                self.password_repeat,
                                            ]
                                        ),
                                        ft.Row(
                                            controls=[self.signup_button, ]
                                        ),
                                    ]
                                )
                            ),
                            ft.Container(
                                width=380,
                                content=ft.Row(
                                    controls=[
                                        ft.Text("¿Ya tienes cuenta?"),
                                        TextLink(
                                            text="¡Inicia Sesión!",
                                            function=lambda _: self.page.go("/login")
                                        ),
                                    ]
                                )
                            ),
                            # This control displays a message to the user when it is necessary
                            self.snackbar,
                        ]
                    )
                ),
            ]
        )

    log.info("Página 'SIGNUP' creada.")

    def __toggle_signup_button_state(self, _: ft.ControlEvent) -> None:
        if all((self.name, self.email.value, self.password.value, self.password_repeat.value)):
            self.signup_button.disabled = False
        else:
            self.signup_button.disabled = True

        self.signup_button.update()

    def __create_account(self, _: ft.ControlEvent) -> None:
        name_input = self.name.value.title().strip()
        email_input = self.email.value.lower().strip()
        password_input = self.password.value.strip()
        repeat_input = self.password_repeat.value.strip()

        # First, check if passwords are not equal
        if password_input != repeat_input:
            self.__display_message(msg="¡Las contraseñas no coinciden!", style=SnackbarStyle.DANGER)
            return

        # Second, validates email & password
        if not all((Validate.is_valid_email(email_input), Validate.is_valid_password(password_input))):
            self.__display_message(
                msg="El correo o la contraseña no son válidos.\nLa contraseña debe tener al menos un número, "
                    "una mayúscula y una minúscula y un tamaño mínimo de 8 caracteres.",
                style=SnackbarStyle.DANGER
            )
            return

        # Check if user already exists
        if session.query(User).filter(User.email == email_input).first():
            log.warning("Creación de usuario fallida: El usuario ya existe.")
            log.debug(f" >>> Datos: '{mask_email(email_input)}' - '{mask_password(password_input)}'")
            self.__display_message(msg="¡El correo electrónico ya existe!", style=SnackbarStyle.DANGER)
            return

        self.__reset_fields()

        # Creates new user instance
        new_user = User(fullname=name_input, email=email_input, password=password_input)
        log.info("Usuario creado con éxito.")
        log.debug(f" >>> {new_user}")

        # Saves user to database
        session.add(new_user)
        session.commit()

        # Provide user feedback
        self.__display_message(
            msg=f"¡Bienvenido/a a Dephokey, {new_user.fullname}!\n¡Ahora ya puedes iniciar sesión!",
            style=SnackbarStyle.SUCCESS
        )
        self.__nav_to_login()

    def __display_message(self, msg: str, style: SnackbarStyle) -> None:
        self.snackbar.change_style(msg=msg, style=style)
        self.snackbar.update()

    def __reset_fields(self) -> None:
        self.name.value = ""
        self.email.value = ""
        self.password.value = ""
        self.password_repeat.value = ""
        self.content.update()

    def __nav_to_login(self) -> None:
        # Display loading page
        self.page.overlay.append(LoadingPage())
        self.page.update()

        # Load login page
        time.sleep(2.5)
        self.page.overlay.clear()
        self.page.go("/login")
