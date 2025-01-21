import flet as ft
import time

from interface.pages import LoadPage  # ---> ImportError (Circular import)

from shared.utils.colors import *


class CustomAppbar(ft.Container):
    def __init__(self) -> None:
        super().__init__()

        # General settings
        self.visible = False
        self.toolbar_height = 70

        # Design settings
        self.bgcolor = bgAppbarColor

        # Leading settings
        self.leading = ft.Icon(ft.Icons.START)
        self.leading_width = 240

        # Searchbar settings
        self.title = ft.Container(
            width=400,
            height=50,
            border_radius=25,
            padding=ft.padding.only(15, 2, 15, 2),
            bgcolor=ft.Colors.with_opacity(0.2, lightColorBackground),
            content=ft.Row(
                spacing=10,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Icon(ft.Icons.SEARCH, color=ft.Colors.with_opacity(0.2, lightColorBackground)),
                    ft.TextField(
                        selection_color=selectionColorFieldText,
                        text_style=ft.TextStyle(
                            color=lightColorBackground
                        ),
                        cursor_color=lightColorBackground,
                        hint_text="buscar contenido...",
                        hint_style=ft.TextStyle(
                            color=ft.Colors.with_opacity(0.2, lightColorBackground)
                        ),
                        border=ft.InputBorder.NONE
                    )
                ]
            )
        )
        self.center_title = True

        # Control settings
        self.actions = [
            ft.Container(
                bgcolor=ft.colors.GREEN,
                content=ft.Row(
                    controls=[
                        ft.IconButton(ft.Icons.SETTINGS),
                        ft.IconButton(ft.Icons.LOGOUT)
                    ]
                )
            )
        ]

        self.content = ft.IconButton(ft.Icons.LOGOUT, on_click=self.logout)

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
