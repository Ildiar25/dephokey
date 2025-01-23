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
            bgcolor=lightColorBackground,
            # padding=ft.padding.only(left=10, top=40, right=240),
            expand=True,
        )

        self.sidebar = CustomSidebar(self.page, self.active_content)
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

        # Page design
        self.page.vertical_alignment = ft.MainAxisAlignment.START
        self.page.horizontal_alignment = ft.CrossAxisAlignment.START
        self.page.appbar.visible = True
        self.page.bottom_appbar.visible = True

        # Dashboard Content
        self.sidebar_content = ft.Column(
            expand=True,
            controls=[
                self.sidebar
            ]
        )
        self.body_content = ft.Column(
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Container(
                    expand=True,
                    bgcolor=ft.Colors.PINK
                )
            ]
        )


        self.body = ft.Column(
            expand=True,
            spacing=0,
            controls=[
                ft.Divider(height=1, thickness=1, color="#F2F2F2"),
                ft.Row(
                    expand=True,
                    controls=[
                        self.sidebar_content, self.body_content
                    ]
                )
            ]
        )

        self.content = ft.Column(
            controls=[
                # Row (sidebar menu & content)
                self.body,
            ]
        )
