from collections.abc import Callable

import flet as ft
import time

from interface.controls.custom_searchbar import CustomSearchBar
from interface.controls import CustomElevatedButton, CustomTextField
from interface.pages.body_content import BodyContent
from interface.pages import LoadPage  # ---> ImportError (Circular import)

from shared.utils.colors import *


class CustomAppbar(ft.AppBar):
    def __init__(self,
                 page: ft.Page,
                 content: BodyContent,
                 search_bar: bool = False,
                 find_function: Callable[[ft.ControlEvent], None] | None = None) -> None:
        super().__init__()

        # General settings
        self.page = page
        self.visible = False
        self.search_bar = search_bar
        self.toolbar_height = 79
        self.settings_content = content
        self.look_for_elements = find_function

        # Settings attributes
        self.fullname = CustomTextField(
            value=self.page.session.get("session").fullname,
            expand=True,
        )
        self.email = CustomTextField(
            value=self.page.session.get("session").email,
            expand=True
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
            content=ft.Image(src="interface/assets/logotype.svg", fit=ft.ImageFit.FIT_WIDTH)
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
        self.settings_content.controls[0].controls[1].controls = []
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
                                    # height=29,
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
                                    # height=140,
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
                                            # on_click=lambda _: self.page.close(self),
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
