import time
from hashlib import sha256

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


class Login(ft.Container):
    """Creates Login page and displays all form elements"""
    def __init__(self, page: ft.Page) -> None:
        super().__init__()

        # Page attributes
        self.page = page
        self.page.scroll = None
        self.snackbar = Snackbar()

        # Login attributes
        self.email = CustomTextField(
            label="Correo Electrónico",
            autofocus=True,
            on_change=self.__toggle_login_button_state,
            max_length=30
        )
        self.password = CustomTextField(
            label="Contraseña",
            on_change=self.__toggle_login_button_state,
            on_submit=self.__login,
            password=True,
            can_reveal_password=True,
            max_length=30
        )
        self.login_button = CustomElevatedButton(
            name="Login",
            style=ButtonStyle.DEFAULT,
            expand=True,
            disabled=True,
            on_click=self.__login
        )

        # Page design
        self.expand = True

        # Body content
        self.content = ft.Row(
            spacing=0,
            controls=[
                # Login form
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
                                height=296,
                                content=ft.Column(
                                    spacing=24,
                                    controls=[
                                        ft.Text(
                                            value="Inicia Sesión en Dephokey",
                                            font_family="AlbertSansB",
                                            color=accentTextColor,
                                            size=24
                                        ),
                                        ft.Column(
                                            controls=[
                                                self.email,
                                                self.password,
                                                TextLink(
                                                    text="¿Has olvidado la contraseña?",
                                                    target=lambda _: self.page.go(r"\reset_password")
                                                ),
                                            ]
                                        ),
                                        ft.Row(
                                            controls=[self.login_button, ]
                                        ),
                                    ]
                                )
                            ),
                            ft.Container(
                                width=380,
                                content=ft.Row(
                                    controls=[
                                        ft.Text("¿No tienes cuenta?"),
                                        TextLink(
                                            text="¡Regístrate en Dephokey!",
                                            target=lambda _: self.page.go(r"\signup")
                                        ),
                                    ]
                                )
                            ),
                            # This control displays a message to the user when it is necessary
                            self.snackbar,
                        ]
                    )
                ),

                # Lateral decoration
                ft.Container(
                    expand=True,
                    image=ft.DecorationImage(r"interface\assets\bg-image-login.png", fit=ft.ImageFit.COVER),
                    content=ft.Stack(
                        alignment=ft.alignment.top_right,
                        controls=[
                            ft.Container(
                                width=152,
                                height=48,
                                margin=ft.margin.only(top=25, right=50),
                                content=ft.Image(r"interface\assets\logotype-white.svg")
                            ),
                            ft.Column(
                                expand=True,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Container(
                                        expand=True,
                                        alignment=ft.alignment.center,
                                        content=ft.Image(src=r"interface\assets\login-account-circle.svg", width=350)
                                    ),
                                ]
                            ),
                        ]
                    )
                ),
            ]
        )

    log.info("Página 'LOGIN' creada.")

    def __toggle_login_button_state(self, _: ft.ControlEvent) -> None:
        if all((self.email.value, self.password.value)):
            self.login_button.disabled = False
        else:
            self.login_button.disabled = True
        self.login_button.update()

    def __login(self, _: ft.ControlEvent) -> None:
        email_input = self.email.value.lower().strip()
        password_input = self.password.value.strip()

        # First, validate email & password
        if not all((Validate.is_valid_email(email_input), Validate.is_valid_password(password_input))):
            self.__display_message(
                msg="El correo o la contraseña no son válidos.\nLa contraseña debe tener al menos un número, "
                    "una mayúscula y una minúscula",
                style=SnackbarStyle.DANGER
            )
            return

        # Second, check if email already exists
        if not session.query(User).filter(User.email == email_input).first():
            self.__display_message(msg="¡El usuario no existe!", style=SnackbarStyle.DANGER)
            return

        # Third, load user and hashed input password
        user: User = session.query(User).filter(User.email == email_input).first()
        hashed_password = sha256(password_input.encode()).hexdigest()

        # Compare data inputs with loaded data
        if not all((user.email == email_input, user.hashed_password == hashed_password)):
            log.warning("Inicio de sesión fallido: Los datos no coinciden.")
            log.debug(f" >>> Datos: '{mask_email(email_input)}' - '{mask_password(password_input)}'")
            self.__display_message(
                msg="El correo electrónico o la contraseña no son válidos.", style=SnackbarStyle.DANGER
            )
            return

        self.__reset_fields()
        self.__create_session(user)
        self.__nav_to_home()

    def __create_session(self, user: User) -> None:
        self.page.session.set(key="session", value=user)
        log.info("Sesión iniciada con éxito.")
        log.debug(f" >>> Usuario: '{mask_email(user.email)}' BIENVENIDO.")

    def __display_message(self, msg: str, style: SnackbarStyle) -> None:
        self.snackbar.change_style(msg=msg, style=style)
        self.snackbar.update()

    def __reset_fields(self) -> None:
        self.email.value = ""
        self.password.value = ""
        self.content.update()

    def __nav_to_home(self) -> None:
        # Display loading page
        self.page.overlay.append(LoadingPage())
        self.page.update()

        # Load sound
        open_session = ft.Audio(src=r"interface\assets\effects\open-session.mp3", autoplay=True)
        self.page.overlay.append(open_session)
        self.page.update()

        # Load home page
        time.sleep(2.5)
        self.page.update()
        self.page.overlay.clear()
        self.page.go(r"\home")
