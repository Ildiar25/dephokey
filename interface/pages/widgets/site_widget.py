import flet as ft
from typing import Callable

from data.db_orm import session

from features.models import Site
from features.encryption.core import decrypt_data

from interface.controls import TextLink, IconLink, IconLinkStyle
from interface.pages.forms.base_form import FormStyle
from interface.pages.forms import DeleteFormStyle, DeleteForm, SiteForm

from shared.utils.masker import mask_password
from shared.utils.colors import *


class SiteWidget(ft.Card):
    def __init__(self, site: Site, page: ft.Page, update_appearance: Callable[[], None]) -> None:
        super().__init__()

        # General attributes
        self.site = site
        self.page = page
        self.update_appearance = update_appearance

        # Widget settings
        self.width = 365
        self.height = 200
        self.elevation = 2
        self.animate_scale = ft.animation.Animation(200, ft.AnimationCurve.EASE_IN_OUT)

        # SiteWidget elements
        self.site_title = ft.Text(self.site.name if self.site.name else "Sin título", font_family="AlbertSansB",
                                  size=18, color=titleSiteWidgetColor)
        self.site_link = TextLink(text=self.site.address, function=lambda _: self.page.launch_url(self.site.address))
        self.site_username = ft.Text(self.site.username, color=textSiteWidgetColor)
        self.site_password = ft.Text(mask_password(decrypt_data(self.site.encrypted_password)))

        # Widget design
        self.color = bgSiteWidgetColor
        self.shape = ft.RoundedRectangleBorder(4)

        # Widget content
        self.content = ft.Container(
            on_hover=self.scale_widget,
            padding=ft.padding.all(24),
            expand=True,
            content=ft.Column(
                spacing=16,
                controls=[
                    # Header
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            self.site_title,
                            ft.Container(
                                content=ft.Row(
                                    spacing=8,
                                    controls=[
                                        IconLink(ft.Icons.EDIT_OUTLINED, IconLinkStyle.LIGHT,
                                                 function=self.open_edit_site_form),
                                        IconLink(ft.Icons.DELETE_OUTLINED, IconLinkStyle.LIGHT,
                                                 function=self.open_delete_form)
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
                                color=primaryIconColor
                            ),
                            self.site_link
                        ]
                    ),
                    ft.Row(
                        spacing=8,
                        controls=[
                            ft.Icon(
                                ft.Icons.ACCOUNT_CIRCLE_ROUNDED,
                                color=primaryIconColor
                            ),
                            self.site_username
                        ]
                    ),

                    # Footer
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Container(
                                on_hover=self.show_password,
                                content=ft.Row(
                                    spacing=8,
                                    controls=[
                                        ft.Icon(
                                            ft.Icons.PASSWORD_ROUNDED,
                                            color=primaryIconColor
                                        ),
                                        self.site_password
                                    ]
                                )
                            ),
                            IconLink(ft.Icons.COPY_ROUNDED, style=IconLinkStyle.LIGHT, function=self.copy_text,
                                     tooltip="copiar contraseña")
                        ]
                    )
                ]
            )
        )

    def scale_widget(self, cursor: ft.ControlEvent) -> None:
        if cursor and self.scale == 1.05:
            self.scale = 1
        else:
            self.scale = 1.05
        self.update()

    def copy_text(self, cursor: ft.ControlEvent) -> None:
        self.page.set_clipboard(decrypt_data(self.site.encrypted_password))
        cursor.control.show_badge()

    def show_password(self, cursor: ft.ControlEvent) -> None:
        if cursor and self.site_password.value == mask_password(decrypt_data(self.site.encrypted_password)):
            self.site_password.value = decrypt_data(self.site.encrypted_password)
        else:
            self.site_password.value = mask_password(decrypt_data(self.site.encrypted_password))
        self.site_password.update()

    def open_edit_site_form(self, _: ft.ControlEvent) -> None:
        self.page.open(
            SiteForm(
                title=f"Editando {self.site.name}", page=self.page, style=FormStyle.EDIT,
                site=self.site, update_changes=self.update_appearance)
        )

    def open_delete_form(self, _: ft.ControlEvent) -> None:
        self.page.open(DeleteForm(self.page, self.delete_site, DeleteFormStyle.SITE))

    def delete_site(self, _: ft.ControlEvent) -> None:
        # New query
        session.query(Site).filter(Site.id == self.site.id).delete()
        session.commit()
        self.update_appearance()
