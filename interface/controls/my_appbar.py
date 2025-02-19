from collections.abc import Callable

import flet as ft
import time

from data.db_orm import session

from features.models.user import User, UserRole

from interface.controls.custom_searchbar import CustomSearchBar
from interface.controls import CustomElevatedButton, CustomTextField

from interface.pages.forms.change_password_form import ChangePasswordForm
# from interface.pages.admin import Admin  # ---> ImportError (Circular import)
from interface.pages.body_content import BodyContent
from interface.pages import LoadPage  # ---> ImportError (Circular import)


from shared.validate import Validate
from shared.utils.colors import *


class CustomAppbar(ft.AppBar):
    def __init__(self,
                 page: ft.Page,
                 content: BodyContent,
                 snackbar: ft.SnackBar,
                 admin_page,  # Admin Class
                 search_bar: bool = False,
                 find_function: Callable[[ft.ControlEvent], None] | None = None) -> None:
        super().__init__()

        # General settings
        self.page = page
        self.admin_page = admin_page
        self.snackbar = snackbar
        self.visible = False
        self.search_bar = search_bar
        self.toolbar_height = 79
        self.settings_content = content
        self.look_for_elements = find_function
        self.user = self.page.session.get("session")

        self.back_button = ft.IconButton(
            ft.Icons.KEYBOARD_DOUBLE_ARROW_LEFT_ROUNDED,
            icon_color=primaryCorporateColor,
            on_click=self.go_back,
            highlight_color=neutral20,
            hover_color=neutral10,
            visible=False
        )

        # Settings attributes
        self.fullname = CustomTextField(
            value=self.page.session.get("session").fullname,
            expand=True,
            on_change=self.toggle_empty_fields
        )
        self.email = CustomTextField(
            value=self.page.session.get("session").email,
            expand=True,
            on_change=self.toggle_empty_fields
        )
        self.password = CustomTextField(
            value="oooooooooooo",
            expand=True,
            password=True,
            read_only=True,
        )

        # Design settings
        self.bgcolor = bgAppbarColor

        # Leading (Logo)
        self.leading_width = 230
        self.leading = ft.Container(
            margin=ft.margin.only(left=24, right=64),
            content=ft.Image(src="interface/assets/logotype-color.svg", fit=ft.ImageFit.FIT_WIDTH)
        )

        # Title (Search bar)
        if self.search_bar and find_function:
            self.center_title = True
            self.title = CustomSearchBar(1008, self.look_for_elements)

        # Options (Settings & Logout)
        self.actions = [
            ft.Container(
                width=72,
                margin=ft.margin.only(left=64, right=56),
                content=ft.Row(
                    controls=[
                        ft.IconButton(
                            ft.Icons.SETTINGS_ROUNDED,
                            icon_color=iconAppbarColor,
                            on_click=self.settings,
                            highlight_color=selectedIconAppbarColor,
                            hover_color=neutral60
                        ),
                        ft.IconButton(
                            ft.Icons.EXIT_TO_APP_ROUNDED,
                            icon_color=iconAppbarColor,
                            on_click=self.logout,
                            highlight_color=selectedIconAppbarColor,
                            hover_color=neutral60
                        )
                    ]
                )
            )
        ]

    def settings(self, _: ft.ControlEvent) -> None:
        self.settings_content.controls[0].controls[0].value = "Configuración"
        self.settings_content.controls[0].controls[1].controls = [self.back_button]
        self.settings_content.update()

        if self.user.role == UserRole.ADMIN:
            self.back_button.visible = True
            self.back_button.update()

        self.settings_content.controls[1].controls = [
            ft.Row(
                spacing=32,
                controls=[
                    ft.Container(
                        height=334,
                        expand=True,
                        bgcolor=bgGeneralFormColor,
                        border_radius=4,
                        padding=24,
                        shadow=ft.BoxShadow(blur_radius=0.9, offset=(0.0, 0.5),
                                    color=ft.Colors.with_opacity(opacity=0.3, color=neutral80)),
                        content=ft.Column(
                            spacing=24,
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Text(
                                            "Información general",
                                            font_family="AlberSansR",
                                            size=24,
                                            color=accentTextColor
                                        ),
                                    ]
                                ),
                                ft.Row(
                                    controls=[
                                        ft.Column(
                                            expand=True,
                                            spacing=8,
                                            controls=[
                                                ft.Text(
                                                    "Nombre completo:",
                                                    font_family="AlbertSansL",
                                                    size=16,
                                                    color=primaryTextColor
                                                ),
                                                ft.Row(controls=[self.fullname]),
                                                ft.Text(
                                                    "Correo electrónico:",
                                                    font_family="AlbertSansL",
                                                    size=16,
                                                    color=primaryTextColor
                                                ),
                                                ft.Row(controls=[self.email])
                                            ]
                                        )
                                    ]
                                ),
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.END,
                                    controls=[
                                        CustomElevatedButton(
                                            name="Guardar",
                                            width=85,
                                            bg_color=bgEButtonColor,
                                            foreground_color=tertiaryTextColor,
                                            on_click=self.update_info,
                                            border_size=-1
                                        )
                                    ]
                                )
                            ]
                        )
                    ),
                    ft.Container(
                        height=334,
                        expand=True,
                        bgcolor=bgGeneralFormColor,
                        border_radius=4,
                        padding=24,
                        shadow=ft.BoxShadow(blur_radius=0.9, offset=(0.0, 0.5),
                                            color=ft.Colors.with_opacity(opacity=0.3, color=neutral80)),
                        content=ft.Column(
                            spacing=24,
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Row(
                                    # height=29,
                                    controls=[
                                        ft.Text(
                                            "Seguridad",
                                            font_family="AlberSansR",
                                            size=24,
                                            color=accentTextColor
                                        ),
                                    ]
                                ),
                                ft.Row(
                                    # height=140,
                                    controls=[
                                        ft.Column(
                                            expand=True,
                                            spacing=8,
                                            controls=[
                                                ft.Text(
                                                    "Contraseña:",
                                                    font_family="AlbertSansL",
                                                    size=16,
                                                    color=primaryTextColor
                                                ),
                                                ft.Row(controls=[self.password]),
                                                ft.Text(
                                                    "",
                                                    font_family="AlbertSansL",
                                                    size=16,
                                                    color=primaryTextColor
                                                ),
                                                ft.Row(controls=[CustomTextField(disabled=True, border_width=0)])
                                            ]
                                        )
                                    ]
                                ),
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.END,
                                    controls=[
                                        CustomElevatedButton(
                                            name="Cambiar contraseña",
                                            foreground_color=secondaryTextColor,
                                            on_click=self.open_change_password_form,
                                            border_size=-1
                                        )
                                    ]
                                )
                            ]
                        )
                    )
                ]
            )
        ]
        self.settings_content.update()

    def update_info(self, _: ft.ControlEvent) -> None:

        new_fullname: str = self.fullname.value.title().strip()
        new_email: str = self.email.value.lower().strip()

        # Check fields
        if all([new_fullname, new_email]):
            # Check if email is valid
            if not Validate.is_valid_email(new_email):
                self.email.error_text = "El correo no es válido."
                self.email.update()

            else:
                user: User = self.page.session.get("session")

                user.fullname = new_fullname
                user.email = new_email
                session.commit()

                # Updates settings page
                self.fullname.value = self.page.session.get("session").fullname
                self.fullname.update()

                self.email.value = self.page.session.get("session").email
                self.email.update()

                # Notifies to the user
                self.snackbar.content.value = f"¡Datos actualizados!"
                self.snackbar.content.color = successTextColor
                self.snackbar.bgcolor = neutralSuccessLight
                self.snackbar.open = True
                self.snackbar.update()

    def open_change_password_form(self, _: ft.ControlEvent) -> None:
        self.page.open(
            ChangePasswordForm(self.page)
        )

    def go_back(self, _: ft.ControlEvent) -> None:
        self.settings_content.controls[0].controls[0].value = "Bienvenido Administrador!"
        self.settings_content.controls[0].controls[1].controls = []
        self.settings_content.controls[1].controls = [self.admin_page]
        self.settings_content.update()


    @staticmethod
    def toggle_empty_fields(field: ft.ControlEvent) -> None:
        if field and not field.control.value:
            field.control.error_text = "El campo no puede estar vacío."
        else:
            field.control.error_text = None
        field.control.update()

    def logout(self, _: ft.ControlEvent) -> None:

        # Close session
        self.page.session.clear()

        # Hide menus
        self.page.appbar.visible = False
        self.page.bottom_appbar.visible = False
        self.page.bgcolor = primaryCorporate100
        self.page.clean()
        self.page.update()

        # Load sound
        close_session = ft.Audio("interface/assets/effects/close-session.mp3", autoplay=True)
        self.page.overlay.append(close_session)
        self.page.update()

        # Show page loading
        self.page.overlay.append(
            LoadPage()
        )
        self.page.update()

        # Load login page
        time.sleep(2.5)
        self.page.overlay.clear()
        self.page.go("/login")
