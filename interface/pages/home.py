import flet as ft

from interface.controls import CustomAppbar, CustomSidebar

from shared.utils.colors import *


class Home(ft.Container):
    def __init__(self, page: ft.Page) -> None:
        super().__init__()

        # General attributes
        self.page = page
        self.page.scroll = ft.ScrollMode.AUTO
        self.active_content = ft.Container(
            padding=ft.padding.only(56, 57, 56),
            height=5000,
            expand=True,
            content=ft.Column(
                controls=[
                    # Title
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text(f"Bienvenido 'usuario'",  # TODO: Show admin name
                                            font_family="AlbertSansB", color=primaryTextColor, size=24)
                                ]
                            )
                        ]
                    )
                ]
            )
        )

        # Sidebar controller & Searchbar function
        self.page.appbar = CustomAppbar(self.active_content, search_bar=True, find_function=self.look_for_elements)
        self.sidebar = CustomSidebar(self.page, self.active_content)

        # Page design
        self.page.bgcolor = neutral05
        self.page.appbar.visible = True
        self.page.bottom_appbar.visible = True

        # Dashboard
        self.content = ft.Column(
            expand=True,
            spacing=0,
            controls=[
                # Divider
                ft.Divider(height=1, thickness=1, color=neutral05),

                # Sidebar & Bodycontent
                ft.Row(
                    spacing=0,
                    expand=True,
                    controls=[
                        # Sidebar
                        ft.Column(
                            width=200,
                            controls=[
                                self.sidebar
                            ]
                        ),
                        # Body content
                        ft.Column(
                            expand=True,
                            scroll=ft.ScrollMode.AUTO,
                            controls=[
                                self.active_content
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
                        title if e.control.value != "" else no_title
                    ]
                ),
                # Content

            ]
        )

        self.active_content.update()
