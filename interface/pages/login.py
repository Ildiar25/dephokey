import flet as ft
import time
from hashlib import sha256

from data.db_orm import session

from features.models.user import User

from interface.pages import LoadPage
from interface.controls import *

from shared.validate import Validate
from shared.logger_setup import main_logger as logger
from shared.utils.masker import mask_email, mask_password
from shared.utils.colors import *


class Login(ft.Container):
    def __init__(self, page: ft.Page) -> None:
        super().__init__()

        # General attributes
        self.page = page
        self.snackbar = ft.SnackBar(
            bgcolor=bgSnackbarDangerColor,
            content=ft.Text(
                "",
                text_align=ft.TextAlign.CENTER,
                color=dangerTextColor
            )
        )

        # Main app settings
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        # Login elements
        self.email = CustomTextField(
            label="Correo Electrónico",
            on_change=self.toggle_login_button_state
        )
        self.password = CustomTextField(
            label="Contraseña",
            on_change=self.toggle_login_button_state,
            password=True,
            can_reveal_password=True
        )
        self.login_button = CustomElevatedButton(
            "Login", bg_color=bgEButtonColor, foreground_color=tertiaryTextColor,
            border_size=-1, expand=True, disabled=True, on_click=self.login
        )

        # Page design
        self.width = 1080
        self.height = 720
        self.border_radius = 10

        # Body content
        self.content = ft.Row(
            spacing=0,
            controls=[
                # Login form
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
                                height=296,
                                content=ft.Column(
                                    spacing=24,
                                    controls=[
                                        ft.Text(
                                            "Inicia Sesión en Dephokey",
                                            font_family="AlbertSansB",
                                            color=accentTextColor,
                                            size=24
                                        ),
                                        ft.Column(
                                            controls=[
                                                self.email,
                                                self.password,
                                                ft.Container(
                                                    on_hover=self.focus_link,
                                                    on_click=lambda _: print("/forgot_password"),
                                                    content=ft.Text(
                                                        "¿Has olvidado la contraseña?",
                                                        color=accentTextColor
                                                    )
                                                )
                                            ]
                                        ),
                                        ft.Row(
                                            controls=[
                                                self.login_button
                                            ]
                                        )
                                    ]
                                )
                            ),
                            ft.Container(
                                width=380,
                                content=ft.Row(
                                    controls=[
                                        ft.Text("¿No tienes cuenta?"),
                                        ft.Container(
                                            on_hover=self.focus_link,
                                            on_click=lambda _: self.page.go("/signup"),
                                            content=ft.Text(
                                                "Regístrate en Dephokey!",
                                                color=accentTextColor
                                            )
                                        )
                                    ]
                                )
                            ),
                            self.snackbar
                        ]
                    )
                ),

                # Image deco
                ft.Container(
                    expand=True,
                    image=ft.DecorationImage("interface/assets/right-bgimage.png", fit=ft.ImageFit.COVER),
                    content=ft.Stack(
                        alignment=ft.alignment.bottom_right,
                        controls=[
                            ft.Container(
                                width=152,
                                height=48,
                                margin=ft.margin.only(0, 0, 50, 25),
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
                                        content=ft.Icon(ft.Icons.LOCK_ROUNDED, size=250, color=iconAccentFormColor)
                                    )
                                ]
                            )
                        ]
                    )
                )
            ]
        )

    logger.info("Creación de la página 'LOGIN' realizada.")

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

    def toggle_login_button_state(self, _: ft.ControlEvent) -> None:
        if all((self.email.value, self.password.value)):
            self.login_button.disabled = False
        else:
            self.login_button.disabled = True
        self.login_button.update()

    def login(self, _: ft.ControlEvent) -> None:

        email_input = self.email.value.lower().strip()
        password_input = self.password.value.strip()

        # First, validate email & password
        if not all((Validate.is_valid_email(email_input), Validate.is_valid_password(password_input))):
            self.snackbar.content.value = ("El correo o la contraseña no son válidos.\n"
                                           "La contraseña debe tener al menos un número, una mayúscula y "
                                           "una minúscula")
            self.snackbar.open = True
            self.snackbar.update()
        else:
            # Second, check if email already exists
            if not session.query(User).filter(User.email == email_input).first():
                self.snackbar.content.value = "¡El usuario no existe!"
                self.snackbar.open = True
                self.snackbar.update()
            else:
                # Third, load user and hashed input password
                user: User = session.query(User).filter(User.email == email_input).first()
                hashed_password = sha256(password_input.encode()).hexdigest()

                # Compare data inputs with loaded data
                if not all((user.email == email_input, user.hashed_password == hashed_password)):
                    logger.warning("Inicio de sesión fallido: Los datos no coinciden...")
                    logger.debug(f" >>> Datos: '{mask_email(email_input)}' - '{mask_password(password_input)}'")
                    self.snackbar.content.value = "El correo electrónico o la contraseña no son válidos."
                    self.snackbar.open = True
                    self.snackbar.update()

                else:
                    # Create new session
                    self.page.session.set("session", user)
                    logger.info("Sesión iniciada con éxito.")
                    logger.debug(f" >>> Usuario: '{mask_email(user.email)}' BIENVENIDO.")

                    # Report page loading
                    self.page.overlay.append(
                        LoadPage()
                    )
                    self.page.update()

                    # Load home page
                    time.sleep(2)
                    self.page.overlay.clear()
                    self.page.go("/home")
