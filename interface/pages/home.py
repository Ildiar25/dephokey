import flet as ft
import time

from interface.controls import CustomAppbar, CustomSidebar
from shared.utils.colors import *


class Home(ft.Container):
    def __init__(self, page: ft.Page) -> None:
        super().__init__()

        # General attributes
        self.page = page
        self.active_content = ft.Container(
            height=5000,
            expand=True,
            bgcolor=lightColorBackground
        )

        # Sidebar controller
        self.sidebar = CustomSidebar(self.page, self.active_content)

        # Page design
        self.page.vertical_alignment = ft.MainAxisAlignment.START
        self.page.horizontal_alignment = ft.CrossAxisAlignment.START
        self.page.appbar.visible = True
        self.page.bottom_appbar.visible = True

        # Dashboard
        self.content = ft.Column(
            expand=True,
            spacing=0,
            controls=[
                # Divider
                ft.Divider(height=1, thickness=1, color="#F2F2F2"),

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

        # self.banner = ft.Banner(
        #     content=ft.Row(
        #         controls=[
        #             ft.Icon(ft.Icons.INFO_ROUNDED, size=45),
        #             ft.ListTile(
        #                 title=ft.Text("ATENCIÓN", font_family="AlbertSansB"),
        #                 subtitle=ft.Text("Hay que tener en cuenta que todos los datos almacenados no deben de ser "
        #                                  "verídicos, pues dicha aplicación no cumple con los estándares de seguridad "
        #                                  "PCI DSS\n(https://stripe.com/es/guides/pci-compliance). Esta aplicación sólo "
        #                                  "es para la verificación del funcionamiento establecido en el briefing del "
        #                                  "proyecto final.")
        #             )
        #         ]
        #     ),
        #     actions=[
        #         ft.TextButton("ACEPTAR")
        #     ]
        # )
