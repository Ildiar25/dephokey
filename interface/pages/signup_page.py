import flet as ft
import time

from data.db_orm import session

from features.models.user import User

from interface.pages.loading_page import LoadingPage
from interface.controls import *

from shared.validate import Validate
from shared.logger_setup import main_log as log
from shared.utils.masker import mask_email, mask_password
from shared.utils.colors import *


class Signup(ft.Container):
    def __init__(self, page: ft.Page) -> None:
        super().__init__()

        # General attributes (like info elements)
        self.page = page
        self.snackbar = Snackbar()

        # Signup attributes
        self.name = CustomTextField(label="Nombre Completo", on_change=self.toggle_signup_button_state, max_length=30)
        self.email = CustomTextField(label="Correo electrónico",
            on_change=self.toggle_signup_button_state, max_length=30)
        self.password = CustomTextField(label="Contraseña", on_change=self.toggle_signup_button_state,
            password=True, can_reveal_password=True, max_length=30)
        self.password_repeat = CustomTextField(label="Repite la contraseña", on_change=self.toggle_signup_button_state,
            password=True, max_length=30)
        self.signup_button = CustomElevatedButton(
            name="Regístrate", style=ButtonStyle.DEFAULT, expand=True, disabled=True, on_click=self.create_account
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
                                    )
                                ]
                            )
                        ]
                    )
                ),

                # Signup form
                ft.Container(
                    expand=True,
                    bgcolor=bgGeneralFormColor,
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
                                        TextLink(
                                            text="¡Inicia Sesión!",
                                            function=lambda _: self.page.go("/login")
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

    log.info("Página 'SIGNUP' creada.")

    def toggle_signup_button_state(self, _: ft.ControlEvent) -> None:
        if all((self.name, self.email.value, self.password.value, self.password_repeat.value)):
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
            # Reset Snackbar
            self.snackbar.change_style(msg="¡Las contraseñas no coinciden!", style=SnackbarStyle.DANGER)
            self.snackbar.update()
            return

        # Second, validates email & password
        if not all((Validate.is_valid_email(email_input), Validate.is_valid_password(password_input))):
            # Reset Snackbar
            self.snackbar.change_style(
                msg="El correo o la contraseña no son válidos.\nLa contraseña debe tener al menos un número, "
                    "una mayúscula y una minúscula", style=SnackbarStyle.DANGER)
            self.snackbar.update()
            return

        # Check if user already exists
        if session.query(User).filter(User.email == email_input).first():
            log.warning("Creación de usuario fallida: El usuario ya existe.")
            log.debug(f" >>> Datos: '{mask_email(email_input)}' - '{mask_password(password_input)}'")

            # Reset Snackbar
            self.snackbar.change_style(msg="¡El correo electrónico ya existe!", style=SnackbarStyle.DANGER)
            self.snackbar.update()
            return

        # Creates new user instance
        new_user = User(fullname=name_input, email=email_input, password=password_input)
        log.info("Usuario creado con éxito.")
        log.debug(f" >>> {new_user}")

        # Reset fields
        self.name.value = ""
        self.email.value = ""
        self.password.value = ""
        self.password_repeat.value = ""
        self.content.update()

        # Saves user to database
        session.add(new_user)
        session.commit()

        # Notifies to the user
        self.snackbar.change_style(msg=f"¡Bienvenido/a {new_user.fullname}!", style=SnackbarStyle.SUCCESS)
        self.snackbar.update()

        # Report loading page
        self.page.overlay.append(
            LoadingPage()
        )
        self.page.update()

        # Load login page
        time.sleep(2)
        self.page.overlay.clear()
        self.page.go("/login")
