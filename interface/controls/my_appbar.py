from collections.abc import Callable

import flet as ft
import time

from interface.controls.custom_searchbar import CustomSearchBar
from interface.pages import LoadPage  # ---> ImportError (Circular import)

from shared.utils.colors import *


class CustomAppbar(ft.AppBar):
    def __init__(self, find_function: Callable[[ft.ControlEvent], None]) -> None:
        super().__init__()

        # General settings
        self.visible = False
        self.toolbar_height = 79
        self.look_for_elements = find_function

        # Design settings
        self.bgcolor = bgAppbarColor

        # Leading (Logo)
        self.leading_width = 200
        self.leading = ft.Container(
            width=152,
            height=48,
            margin=ft.margin.only(left=24, right=64),
            image=ft.DecorationImage("interface/assets/logo.png", fit=ft.ImageFit.COVER)
        )

        # Title (Search bar)
        self.center_title = True
        self.title = CustomSearchBar(1008, self.look_for_elements)

        # Options (Logout)
        self.actions = [
            ft.Container(
                width=72,
                margin=ft.margin.only(left=64, right=56),
                content=ft.Row(
                    controls=[
                        ft.IconButton(
                            ft.Icons.SETTINGS_ROUNDED,
                            icon_color=textColorAppbar
                        ),
                        ft.IconButton(
                            ft.Icons.EXIT_TO_APP_ROUNDED,
                            icon_color=textColorAppbar,
                            on_click=self.logout
                        )
                    ]
                )
            )
        ]

    def logout(self, _: ft.ControlEvent) -> None:

        # Close session
        self.page.session.clear()

        # Hide menus
        self.page.appbar.visible = False
        self.page.bottom_appbar.visible = False
        self.page.clean()
        self.page.update()

        # Show page loading
        self.page.overlay.append(
            LoadPage()
        )
        self.page.update()

        # Load login page
        time.sleep(0.5)
        self.page.overlay.clear()
        self.page.go("/login")
