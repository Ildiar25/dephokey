import flet as ft
import time

from data.db_orm import session

from features.models import Site

from interface.pages.forms import DeleteFormStyle, DeleteForm

from shared.utils.masker import mask_password
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

        # SiteWidget elements
        self.title = ft.Text(
            self.site.name if self.site.name else "Sin título",
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
        self.site_password = ft.Text(
            mask_password(self.site.encrypted_password)  # TODO: Decrypt password HERE!
        )
        self.copy_button = ft.Container(
            visible=False,
            on_click=lambda _:self.page.set_clipboard(self.site_password.value),
            padding=ft.padding.only(3),
            content=ft.Icon(
                ft.Icons.COPY_ROUNDED,
                size=18
            )
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
                                            ft.Icons.EDIT_OUTLINED,
                                            color=iconAccentSiteWidgetColor
                                            )
                                        ),
                                        ft.Container(
                                            on_hover=self.toggle_icon_color,
                                            on_click=self.open_delete_form,
                                            content=ft.Icon(
                                                ft.Icons.DELETE_OUTLINE_ROUNDED,
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
                            ft.Icon(
                                ft.Icons.LINK_ROUNDED,
                                color=iconSiteWidgetColor
                            ),
                            self.site_link
                        ]
                    ),
                    ft.Row(
                        spacing=8,
                        controls=[
                            ft.Icon(
                                ft.Icons.ACCOUNT_CIRCLE_ROUNDED,
                                color=iconSiteWidgetColor
                            ),
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
                                        ft.Icon(
                                            ft.Icons.PASSWORD_ROUNDED,
                                            color=iconSiteWidgetColor
                                        ),
                                        self.site_password,
                                        self.copy_button
                                    ]
                                )
                            ),
                            ft.Container(
                                on_hover=self.focus_link,
                                on_click=self.show_password,
                                tooltip="Muestra la contraseña durante 3 segundos",
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

    @staticmethod
    def toggle_icon_color(cursor: ft.ControlEvent) -> None:
        if cursor and cursor.control.content.color == iconAccentSiteWidgetColor:
            cursor.control.content.color = iconSiteWidgetColor
        else:
            cursor.control.content.color = iconAccentSiteWidgetColor
        cursor.control.update()

    def copy_text(self, cursor: ft.ControlEvent) -> None:
        self.page.set_clipboard(self.site_password.value)
        cursor.control.badge = ft.Badge(
            text="Copiado!",
            bgcolor=ft.Colors.with_opacity(opacity=0.5, color=neutral80),
            text_color=neutral05
        )
        cursor.control.update()
        time.sleep(1)
        cursor.control.badge.label_visible = False
        cursor.control.update()

    def show_password(self, cursor: ft.ControlEvent) -> None:
        if cursor:
            self.site_password.value = self.site.encrypted_password  # TODO: Decrypt password HERE!
            self.site_password.update()
            self.copy_button.visible = True
            # self.copy_button.disabled = False
            self.copy_button.update()
            time.sleep(3)
            self.site_password.value = mask_password(self.site.encrypted_password)  # TODO: Decrypt password HERE!
            self.copy_button.visible = False
            # self.copy_button.disabled = True
            self.copy_button.update()

        self.site_password.update()

    def open_delete_form(self, _: ft.ControlEvent) -> None:
        self.page.open(DeleteForm(self.page, self.site, self.delete_site, DeleteFormStyle.SITE))

    def delete_site(self, _: ft.ControlEvent) -> None:
        # New query
        session.query(Site).filter(Site.id == self.site.id).delete()
        session.commit()
