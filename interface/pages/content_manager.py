import flet as ft
from typing import List, Union
from enum import Enum

from features.models.user import User

from interface.controls.snackbar import Snackbar
from interface.pages.page_content import *
from shared.utils.colors import *


class ContentStyle(Enum):
    HOME = "home"
    ADMIN = "admin"
    SITES = "sites"
    CREDITCARDS = "creditcards"
    NOTES = "notes"
    ABOUT = "about"
    SETTINGS = "settings"
    RESULTS = "results"
    EMPTY = "empty"


class BodyContent(ft.Column):
    def __init__(self, page: ft.Page, snackbar: Snackbar, style: ContentStyle = ContentStyle.EMPTY,
                 title: str = "", buttons: Union[List[ft.Control], None] = None) -> None:
        super().__init__()

        # General attributes
        self.page = page
        self.snackbar = snackbar
        self.style = style
        self.title = ft.Text(value=title, font_family="AlbertSansB", color=primaryTextColor, size=24)

        # BodyContent attributes
        self.user: User = self.page.session.get("session")
        self.header = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[self.title, ft.Row(spacing=16, controls=buttons)]
        )
        self.body = ft.Row(expand=True, wrap=True, spacing=16)
        self.results_style = None

        # Body content
        self.home_content = None
        self.admin_content = None
        self.sites_content = None
        self.creditcards_content = None
        self.notes_content = None
        self.about_content = None
        self.settings_content = None
        self.results_content = None

        # Body design
        self.spacing = 32
        self.scroll = ft.ScrollMode.AUTO
        self.expand = True

        # Body content
        self.controls = [self.header, self.body]
        self.__update_appearance()

    def __update_appearance(self, user_input: str | None = None) -> None:
        match self.style:
            case ContentStyle.HOME:
                if not isinstance(self.home_content, HomePage):
                    self.home_content = HomePage(self.page, self.snackbar, self.update_changes)
                    self.body.controls = [self.home_content]
                self.home_content.update_content()
                self.body.controls = [self.home_content]

            case ContentStyle.ADMIN:
                if not isinstance(self.admin_content, AdminPage):
                    self.admin_content = AdminPage(self.page, self.snackbar, self.update_changes)
                    self.body.controls = [self.admin_content]
                self.admin_content.update_content()
                self.body.controls = [self.admin_content]

            case ContentStyle.SITES:
                if not isinstance(self.sites_content, SitesPage):
                    self.sites_content = SitesPage(self.page, self.snackbar, self.update_changes)
                    self.body.controls = [self.sites_content]
                self.sites_content.update_content()
                self.body.controls = [self.sites_content]

            case ContentStyle.CREDITCARDS:
                if not isinstance(self.creditcards_content, CreditcCardsPage):
                    self.creditcards_content = CreditcCardsPage(self.page, self.snackbar, self.update_changes)
                    self.body.controls = [self.creditcards_content]
                self.creditcards_content.update_content()
                self.body.controls = [self.creditcards_content]

            case ContentStyle.NOTES:
                if not isinstance(self.notes_content, NotesPage):
                    self.notes_content = NotesPage(self.page, self.snackbar, self.update_changes)
                    self.body.controls = [self.notes_content]
                self.notes_content.update_content()
                self.body.controls = [self.notes_content]

            case ContentStyle.ABOUT:
                if not isinstance(self.about_content, AboutPage):
                    self.about_content = AboutPage(self.page, self.snackbar, self.update_changes)
                    self.body.controls = [self.about_content]
                self.about_content.update_content()
                self.body.controls = [self.about_content]

            case ContentStyle.SETTINGS:
                if not isinstance(self.settings_content, SettingsPage):
                    self.settings_content = SettingsPage(self.page, self.snackbar)
                    self.body.controls = [self.settings_content]
                self.settings_content.update_content()
                self.body.controls = [self.settings_content]

            case ContentStyle.RESULTS:
                if not isinstance(self.results_content, ResultsPage):
                    self.results_content = ResultsPage(self.page, self.snackbar, self.update_changes)
                    self.body.controls = [self.results_content]
                self.results_content.get_user_input(user_input)
                self.results_content.update_content()
                self.body.controls = [self.results_content]

            case ContentStyle.EMPTY:
                self.header.controls[1].controls.clear()
                self.body.controls.clear()

    def change_content(self, title: str, style: ContentStyle, buttons: Union[List[ft.Control], None] = None) -> None:
        self.style = style
        self.title.value = title
        self.header.controls[1].controls = buttons
        self.__update_appearance()

    def show_results(self, user_input: str) -> None:
        self.style = ContentStyle.RESULTS
        self.title.value = f"Buscando '{user_input}'..."
        self.header.controls[1].controls.clear()
        self.__update_appearance(user_input)

    def update_changes(self) -> None:
        self.__update_appearance()
        self.update()
