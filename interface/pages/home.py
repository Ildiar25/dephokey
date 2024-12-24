import flet as ft
import time

from shared.utils.colors import *


class Home(ft.Container):
    def __init__(self, page: ft.Page) -> None:
        super().__init__()

        # General attributes
        self.page = page
        self.banner = ft.Banner(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.INFO_ROUNDED, size=45),
                    ft.ListTile(
                        title=ft.Text("ATENCIÓN", font_family="AlbertSansB"),
                        subtitle=ft.Text("Hay que tener en cuenta que todos los datos almacenados no deben de ser "
                                         "verídicos, pues dicha aplicación no cumple con los estándares de seguridad "
                                         "PCI DSS\n(https://stripe.com/es/guides/pci-compliance). Esta aplicación sólo "
                                         "es para la verificación del funcionamiento establecido en el briefing del "
                                         "proyecto final.")
                    )
                ]
            ),
            actions=[
                ft.TextButton("ACEPTAR", on_click=lambda _: self.close_banner())
            ]
        )

        # Page design
        self.page.vertical_alignment = ft.MainAxisAlignment.START
        self.page.horizontal_alignment = ft.CrossAxisAlignment.START
        self.page.floating_action_button.visible = True
        self.page.appbar.visible = True
        self.page.update()

        # Dashboard Content
        self.active_content = ft.Container(
            bgcolor=lightColorBackground,
            # padding=ft.padding.only(left=10, top=40, right=240),
            expand=True,
        )

        self.content = ft.Row(
            # height=self.page.window.height,
            spacing=0,
            controls=[
                self.banner,
                # NavRail(page, self.active_content),
                ft.Column(
                    # width=self.page.window.width,
                    expand=True,
                    alignment=ft.MainAxisAlignment.START,
                    controls=[
                        self.active_content,

                    ]
                )
            ]
        )

        self.open_banner()

    def open_banner(self) -> None:
        time.sleep(4)
        self.banner.open = True
        self.page.update()

    def close_banner(self) -> None:
        self.banner.open = False
        self.page.update()
