import time

import flet as ft

from features.models.user import User, UserRole
from interface.controls.searchbar import CustomSearchBar
from interface.pages.content_manager import BodyContent, ContentStyle
from interface.pages.loading_page import LoadingPage
from shared.logger_setup import main_log as log
from shared.utils.colors import (
    neutral05,
    neutral10,
    neutral20,
    neutral60,
    neutral80,
    primaryCorporate100,
    primaryCorporateColor,
)


class CustomAppbar(ft.AppBar):
    def __init__(self, page: ft.Page, snackbar: ft.SnackBar, content: BodyContent) -> None:
        super().__init__()

        # General settings
        self.page = page
        self.snackbar = snackbar

        # Appbar attributes
        self.user: User = self.page.session.get("session")
        self.body_content = content
        self.search_bar = CustomSearchBar(width=1008, function=self.search_results)

        # Appbar design
        self.visible = False
        self.toolbar_height = 79
        self.user = self.page.session.get("session")

        self.back_button = ft.IconButton(
            ft.Icons.KEYBOARD_DOUBLE_ARROW_LEFT_ROUNDED,
            icon_color=primaryCorporateColor,
            on_click=self.go_back,
            highlight_color=neutral20,
            hover_color=neutral10,
            visible=False
        )

        # Design settings
        self.bgcolor = neutral80

        # Leading (Logo)
        self.leading_width = 230
        self.leading = ft.Container(
            margin=ft.margin.only(left=24, right=64),
            content=ft.Image(src="interface/assets/logotype-color.svg", fit=ft.ImageFit.FIT_WIDTH)
        )

        # Title (Search bar)
        self.title = self.search_bar if self.user.role == UserRole.CLIENT else None
        self.center_title = True

        # Options (Settings & Logout)
        self.actions = [
            ft.Container(
                width=72,
                margin=ft.margin.only(left=64, right=56),
                content=ft.Row(
                    controls=[
                        ft.IconButton(
                            ft.Icons.SETTINGS_ROUNDED,
                            icon_color=neutral05,
                            on_click=self.show_settings,
                            highlight_color=primaryCorporateColor,
                            hover_color=neutral60,
                            focus_color=neutral60
                        ),
                        ft.IconButton(
                            ft.Icons.EXIT_TO_APP_ROUNDED,
                            icon_color=neutral05,
                            on_click=self.logout,
                            highlight_color=primaryCorporateColor,
                            hover_color=neutral60,
                            focus_color=neutral60
                        )
                    ]
                )
            )
        ]

    def show_settings(self, _: ft.ControlEvent) -> None:
        log.info("Redirigiendo a SETTINGS")
        buttons = [
            ft.IconButton(
                ft.Icons.KEYBOARD_DOUBLE_ARROW_LEFT_ROUNDED,
                icon_color=primaryCorporateColor,
                on_click=self.go_back,
                highlight_color=neutral20,
                hover_color=neutral10,
                focus_color=neutral10,
                visible=False if self.user.role == UserRole.CLIENT else True
            )
        ]
        self.body_content.change_content(title="Configuración", style=ContentStyle.SETTINGS, buttons=buttons)
        self.body_content.update()

    def go_back(self, _: ft.ControlEvent) -> None:
        log.info("Redirigiendo a ADMIN.")
        self.body_content.change_content(
            title=f"Bienvenido {self.user.fullname.split(' ')[0]}!", style=ContentStyle.ADMIN)
        self.body_content.update()

    def search_results(self, result: ft.ControlEvent) -> None:
        log.info("Redirigiendo a RESULTS")
        self.body_content.show_results(result.control.value.strip())
        self.body_content.update()

    def logout(self, _: ft.ControlEvent) -> None:
        log.info("Sesión cerrada. Redirigiendo a LOGIN.")
        # Close session
        self.page.session.clear()

        # Hide menus
        self.page.appbar.visible = False
        self.page.bottom_appbar.visible = False
        self.page.bgcolor = primaryCorporate100
        self.page.clean()
        self.page.update()

        # Load sound
        close_session = ft.Audio(src="interface/assets/effects/close-session.mp3", autoplay=True)
        self.page.overlay.append(close_session)
        self.page.update()

        # Show page loading
        self.page.overlay.append(
            LoadingPage()
        )
        self.page.update()

        # Load login page
        time.sleep(2.5)
        self.page.overlay.clear()
        self.page.go("/login")
