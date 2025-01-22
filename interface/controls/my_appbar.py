import flet as ft
import time

from interface.controls.custom_searchbar import CustomSearchBar
from interface.pages import LoadPage  # ---> ImportError (Circular import)

from shared.utils.colors import *


class CustomAppbar(ft.AppBar):
    def __init__(self) -> None:
        super().__init__()

        # General settings
        self.visible = True
        self.toolbar_height = 79

        # Design settings
        self.bgcolor = bgAppbarColor

        # Leading (Logo)
        self.leading_width = 200
        self.leading = None  # Load image logo

        # Title (Search bar)
        self.center_title = True
        self.title = CustomSearchBar(1008, self.look_for_elements)

        # Options (Logout)
        self.actions = [
            ft.IconButton(ft.Icons.SETTINGS),
            ft.IconButton(ft.Icons.LOGOUT)
        ]
        # Searchbar settings
        # self.title = ft.Container(
        #     content=ft.Row(
        #         spacing=10,
        #         vertical_alignment=ft.CrossAxisAlignment.CENTER,
        #         controls=[
        #             ft.Icon(ft.Icons.SEARCH, color=ft.Colors.with_opacity(0.2, lightColorBackground)),
        #             ft.TextField(
        #                 selection_color=selectionColorFieldText,
        #                 text_style=ft.TextStyle(
        #                     color=lightColorBackground
        #                 ),
        #                 cursor_color=lightColorBackground,
        #                 hint_text="buscar contenido...",
        #                 hint_style=ft.TextStyle(
        #                     color=ft.Colors.with_opacity(0.2, lightColorBackground)
        #                 ),
        #                 border=ft.InputBorder.NONE
        #             )
        #         ]
        #     )
        # )

    def look_for_elements(self, _: ft.ControlEvent) -> None:
        pass

    def logout(self, _: ft.ControlEvent) -> None:

        # Close session
        self.page.session.clear()
        self.page.update()

        # Report page loading
        self.page.overlay.append(
            LoadPage()
        )
        self.page.update()

        # Load login page
        time.sleep(1)
        self.page.overlay.clear()
        self.page.go("/login")
