import flet as ft

from data.db_orm import session

from features.models.user import User, UserRole
from features.models import *

from interface.controls import CustomTextField, CustomAppbar, CustomElevatedButton, CustomSwitch
from interface.pages.body_content import BodyContent

from shared.validate import Validate
from shared.utils.colors import *


class Admin(ft.Container):
    def __init__(self, page: ft.Page) -> None:
        super().__init__()

        # General attributes
        self.page = page
        self.page.scroll = ft.ScrollMode.AUTO
        self.user = self.page.session.get("session").fullname

        self.snackbar = ft.SnackBar(
            bgcolor=bgSnackbarDangerColor,
            content=ft.Text(
                "",
                text_align=ft.TextAlign.CENTER,
                color=dangerTextColor
            )
        )

        # User form elements
        self.username = CustomTextField(
            label="Nombre Completo",
            expand=True,
            on_change=self.toggle_user_button_state
        )
        self.useremail = CustomTextField(
            label="Correo Electrónico",
            expand=True,
            on_change=self.toggle_user_button_state
        )
        self.userpassword = CustomTextField(
            label="Contraseña",
            expand=True,
            password=True,
            can_reveal_password=True,
            on_change=self.toggle_user_button_state
        )
        self.userswitch = CustomSwitch(
                "Es admin.", 150
            )
        self.useradmin = ft.Container(
            width=200,
            content=self.userswitch
        )

        # CreditCard form elements

        # New User form
        self.add_user_form = ft.Container(
            height=256,
            padding=ft.padding.all(32),
            bgcolor=bgGeneralFormColor,
            border_radius=4,
            shadow=ft.BoxShadow(blur_radius=0.9, offset=(0.0, 0.6),
                                color=ft.Colors.with_opacity(0.3, neutral80)),
            content=ft.Column(
                spacing=32,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text(
                                "Nuevo usuario:",
                                font_family="AlbertSansB",
                                size=18,
                                color=accentTextColor
                            )
                        ]
                    ),
                    ft.Row(
                        spacing=16,
                        controls=[
                            self.username,
                            self.useremail,
                            self.userpassword,
                            self.useradmin
                        ]
                    ),
                    ft.Row(
                        controls=[
                            CustomElevatedButton(
                                "Añadir",
                                icon=ft.Icons.ADD_ROUNDED,
                                foreground_color=tertiaryTextColor,
                                bg_color=primaryCorporateColor,
                                border_size=-1,
                                expand=True,
                                disabled=True,
                                on_click=self.add_new_user
                            )
                        ]
                    )
                ]
            )
        )

        # New Creditcard form
        self.add_creditcard_form = ft.Container(
            height=256,
            padding=ft.padding.all(32),
            bgcolor=bgGeneralFormColor,
            border_radius=4,
            shadow=ft.BoxShadow(blur_radius=0.9, offset=(0.0, 0.6),
                                color=ft.Colors.with_opacity(0.3, neutral80)),
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text(
                                "Nueva tarjeta de crédito:",
                                font_family="AlbertSansB",
                                size=18,
                                color=accentTextColor
                            )
                        ]
                    ),
                    ft.Row(

                    ),
                    ft.Row(
                        controls=[
                            CustomElevatedButton(
                                "Añadir",
                                icon=ft.Icons.ADD_ROUNDED,
                                foreground_color=tertiaryTextColor,
                                bg_color=primaryCorporateColor,
                                border_size=-1,
                                expand=True,
                                disabled=True,
                                on_click=self.add_new_creditcard
                            )
                        ]
                    )
                ]
            )
        )

        # Admin SHOWS
        self.user_content = ft.Container()

        self.active_content = ft.Container(
            padding=ft.padding.only(56, 57, 56),
            content=BodyContent(
                "Bienvenido Administrador"
            )
        )

        # Searchbar function
        self.page.appbar = CustomAppbar(self.active_content)

        # Page design
        self.page.bgcolor = neutral05
        self.page.appbar.visible = True
        self.page.bottom_appbar.visible = True

        # Dashboard
        self.content = ft.Column(
            spacing=0,
            controls=[
                # Divider
                ft.Divider(height=1, thickness=1, color=neutral05),

                # Bodycontent
                ft.Row(
                    spacing=0,
                    expand=True,
                    controls=[
                        ft.Column(
                            expand=True,
                            controls=[
                                # Body content
                                self.active_content,
                                self.snackbar
                            ]
                        )
                    ]
                )
            ]
        )

    def look_for_elements(self, e: ft.ControlEvent) -> None:

        title = ft.Text(
            f"Resultados de '{e.control.value}'",
            font_family="AlbertSansB",
            color=primaryTextColor,
            size=24
        )
        no_title = ft.Text(
            "Nada que mostrar",
            font_family="AlbertSansB",
            color=primaryTextColor,
            size=24
        )

        self.active_content.content = ft.Column(
            controls=[
                # Title
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        title if e.control.value != "" else no_title,
                    ]
                ),

                # Content

            ]
        )

        self.active_content.update()

    def toggle_user_button_state(self, _: ft.ControlEvent) -> None:
        if all((self.username.value, self.useremail.value, self.userpassword.value)):
            self.add_user_form.content.controls[2].controls[0].disabled = False
        else:
            self.add_user_form.content.controls[2].controls[0].disabled = True
        self.add_user_form.content.controls[2].controls[0].update()

    def add_new_user(self, _: ft.ControlEvent) -> None:

        name_input = self.username.value.title().strip()
        email_input = self.useremail.value.lower().strip()
        password_input = self.userpassword.value.strip()

        # First, validates email & password
        if not all((Validate.is_valid_email(email_input), Validate.is_valid_password(password_input))):
            # Reset Snackbar
            self.snackbar.content.color = dangerTextColor
            self.snackbar.bgcolor = bgSnackbarDangerColor
            self.snackbar.update()

            self.snackbar.content.value = ("El correo o la contraseña no son válidos.\n"
                                           "La contraseña debe tener al menos un número, una mayúscula y "
                                           "una minúscula")
            self.snackbar.open = True
            self.snackbar.update()
        else:
            # Check if user already exists
            if session.query(User).filter(User.email == email_input).first():
                # Reset Snackbar
                self.snackbar.content.color = dangerTextColor
                self.snackbar.bgcolor = bgSnackbarDangerColor
                self.snackbar.update()

                self.snackbar.content.value = "¡El correo electrónico ya existe!"
                self.snackbar.open = True
                self.snackbar.update()
            else:
                # Creates new user instance
                new_user = User(fullname=name_input, email=email_input, password=password_input,
                                user_role=UserRole.ADMIN if self.userswitch.get_value() else UserRole.CLIENT)

                # Reset fields
                self.username.value = ""
                self.useremail.value = ""
                self.userpassword.value = ""
                self.userswitch.set_value(False)
                self.add_user_form.update()

                # Saves user to database
                session.add(new_user)
                session.commit()

                # Notifies to the admin
                self.snackbar.content.value = f"¡Usuario {new_user.fullname} agregado!"
                self.snackbar.content.color = successTextColor
                self.snackbar.bgcolor = neutralSuccessLight
                self.snackbar.open = True
                self.snackbar.update()

    def add_new_creditcard(self, _: ft.ControlEvent) -> None:
        pass