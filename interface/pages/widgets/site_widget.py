import flet as ft

from features.models import Site

from interface.pages.forms import DeleteForm
from shared.utils.colors import *


class SiteWidget(ft.Card):
    def __init__(self, site: Site, page: ft.Page) -> None:
        super().__init__()

        # General attributes
        self.site = site
        self.page = page

        # Widget settings
        self.width = 365
        self.height = 200
        self.elevation = 2

        # Sitewidget elements
        self.title = ft.Text(
            self.site.name if self.site.name else "Título de la web",
            font_family="AlbertSansB",
            size=18,
            color=titleSiteWidgetColor
        )
        self.site_link = ft.Container(
            on_hover=self.focus_link,
            on_click=lambda _: self.page.launch_url(self.site.address),
            content=ft.Text(
                self.site.address,
                color=textSiteWidgetColor
            )
        )
        self.site_username = ft.Text(
            self.site.username,
            color=textSiteWidgetColor
        )


        # Widget design
        self.color = bgSiteWidgetColor
        self.shape = ft.RoundedRectangleBorder(4)

        # Widget content
        self.content = ft.Container(
            padding=ft.padding.all(24),
            expand=True,
            content=ft.Column(
                spacing=16,
                controls=[

                    # Title
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            self.title,
                            ft.Container(
                                content=ft.Row(
                                    spacing=8,
                                    controls=[
                                        ft.Container(
                                            on_hover=self.toggle_icon_color,
                                            content=ft.Icon(
                                            ft.Icons.EDIT,
                                            color=iconAccentSiteWidgetColor
                                            )
                                        ),
                                        ft.Container(
                                            on_hover=self.toggle_icon_color,
                                            on_click=self.open_delete_form,
                                            content=ft.Icon(
                                                ft.Icons.DELETE,
                                                color=iconAccentSiteWidgetColor
                                            )
                                        )
                                    ]
                                )
                            )
                        ]
                    ),

                    # Body
                    ft.Row(
                        spacing=8,
                        controls=[
                            ft.Icon(ft.Icons.WEB),
                            self.site_link
                        ]
                    ),
                    ft.Row(
                        spacing=8,
                        controls=[
                            ft.Icon(ft.Icons.SUPERVISED_USER_CIRCLE_ROUNDED),
                            self.site_username
                        ]
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Container(
                                content=ft.Row(
                                    spacing=8,
                                    controls=[
                                        ft.Icon(ft.Icons.PASSWORD_ROUNDED),
                                        ft.Text(self.site.encrypted_password)
                                    ]
                                )
                            ),
                            ft.Container(
                                on_hover=self.focus_link,
                                on_click=lambda _: print(f"Mostrando Contraseña"),
                                content=ft.Text(
                                    "ver contraseña",
                                    color=accentTextColor
                                )
                            )
                        ]
                    )
                ]
            )
        )

    @staticmethod
    def focus_link(cursor: ft.ControlEvent) -> None:
        if cursor and cursor.control.content.color == accentTextColor:
            cursor.control.content.color = textSiteWidgetColor
        else:
            cursor.control.content.color = accentTextColor
        cursor.control.update()

    def open_delete_form(self, _: ft.ControlEvent) -> None:
        self.page.open(DeleteForm(self.page, self.site, self.delete_site))

    def delete_site(self, _: ft.ControlEvent) -> None:
        print("Deleting objeeeect....")

    @staticmethod
    def toggle_icon_color(cursor: ft.ControlEvent) -> None:
        if cursor and cursor.control.content.color == iconAccentSiteWidgetColor:
            cursor.control.content.color = iconSiteWidgetColor
        else:
            cursor.control.content.color = iconAccentSiteWidgetColor
        cursor.control.update()

