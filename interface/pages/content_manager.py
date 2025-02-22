import flet as ft
from typing import List, Union
from enum import Enum

from interface.controls.snackbar import Snackbar
from interface.pages.settings_content import SettingsPage
from interface.pages.widgets import SiteWidget, NoteWidget
from shared.utils.colors import *


class ContentStyle(Enum):
    HOME = "home"
    ADMIN = "admin"
    SITES = "sites"
    CREDITCARDS = "creditcards"
    NOTES = "notes"
    ABOUT = "about"
    SETTINGS = "settings"
    EMPTY = "empty"


class BodyContent(ft.Column):
    def __init__(self, page: ft.Page, snackbar: Snackbar, style: ContentStyle = ContentStyle.EMPTY,
                 title: str = "", buttons: Union[List[ft.Control], None] = None) -> None:
        super().__init__()

        # General attributes
        self.page = page
        self.snackbar = snackbar
        self.style = style

        # BodyContent attributes
        self.user = self.page.session.get("session")
        self.header = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text(value=title, font_family="AlbertSansB", color=primaryTextColor, size=24),
                ft.Row(spacing=16, controls=buttons)
            ]
        )
        self.body = ft.Row(expand=True, wrap=True, spacing=16)
        self.style = None

        # Body design
        self.spacing = 32
        self.scroll = ft.ScrollMode.AUTO
        self.expand = True

        # Body content
        self.controls = [
            self.header,
            self.body
        ]

        self.update_appearance()

    def change_content(self, title: str, style: ContentStyle, buttons: Union[List[ft.Control], None] = None) -> None:
        self.style = style
        self.header.controls[0].value = title
        self.header.controls[1].controls = buttons
        self.update_appearance()

    def update_changes(self) -> None:
        self.user = self.page.session.get("session")
        self.update_appearance()
        self.update()

    def update_appearance(self) -> None:
        self.user = self.page.session.get("session")
        match self.style:
            case ContentStyle.HOME:
                self.body.controls = []

            case ContentStyle.ADMIN:
                self.body.controls = []

            case ContentStyle.SITES:
                self.body.controls = [SiteWidget(site, self.page, self.update_changes) for site in self.user.sites]

            case ContentStyle.CREDITCARDS:
                self.body.controls = []

            case ContentStyle.NOTES:
                self.body.controls = [NoteWidget(note, self.page, self.update_changes) for note in self.user.notes]

            case ContentStyle.ABOUT:
                self.body.controls = []

            case ContentStyle.SETTINGS:
                self.body.controls = [SettingsPage(self.page, self.snackbar)]

            case ContentStyle.EMPTY:
                self.header.controls[1].controls.clear()
                self.body.controls.clear()
