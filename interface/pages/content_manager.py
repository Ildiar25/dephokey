from enum import Enum

import flet as ft

from features.models.user import User
from interface.controls.snackbar import Snackbar
from interface.pages.page_content import (
    AboutPage,
    AdminPage,
    CreditcCardsPage,
    EntriesPage,
    HomePage,
    NotesPage,
    SettingsPage,
    SitesPage,
)
from shared.logger_setup import main_log as log
from shared.utils.colors import primaryTextColor


class ContentStyle(Enum):
    ABOUT = "about"
    ADMIN = "admin"
    CREDITCARDS = "creditcards"
    EMPTY = "empty"
    ENTRIES = "entries"
    HOME = "home"
    NOTES = "notes"
    SETTINGS = "settings"
    SITES = "sites"


class ContentManager(ft.Column):
    """
    Content manager provides functionality to manage content for all instantiated pages.
    Otherwise, only if page exists update their content.
    """
    def __init__(
            self,
            page: ft.Page,
            snackbar: Snackbar,
            style: ContentStyle = ContentStyle.EMPTY,
            title: str = "",
            buttons: list[ft.Control] | None = None
    ) -> None:
        super().__init__()

        # General attributes
        self.page = page
        self.snackbar = snackbar
        self.style = style

        # ContentManager attributes
        self.user: User = self.page.session.get("session")
        self.title = ft.Text(
            value=title,
            font_family="AlbertSansB",
            color=primaryTextColor,
            size=24
        )
        self.buttons = ft.Row(spacing=16, controls=buttons)

        # Body attributes
        self.header = ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[self.title, self.buttons])
        self.canvas = ft.Row(expand=True, wrap=True, spacing=16)

        # Displayed main pages
        self.about_pg = None
        self.admin_pg = None
        self.creditcard_pg = None
        self.entries_pg = None
        self.home_pg = None
        self.note_pg = None
        self.settings_pg = None
        self.sites_pg = None

        # Body design
        self.spacing = 32
        self.scroll = ft.ScrollMode.AUTO
        self.expand = True

        # ContentManager content
        self.controls = [self.header, self.canvas]

        self.__update_appearance()

        log.info("Inicializando 'CONTENT MANAGER'...")

    def __update_appearance(self, user_input: str | None = None) -> None:
        match self.style:
            case ContentStyle.ABOUT:
                if not isinstance(self.about_pg, AboutPage):
                    self.about_pg = AboutPage(self.page, self.snackbar, self.__confirm_changes)
                    self.canvas.controls = [self.about_pg]
                    log.info("Página 'ABOUT' creada.")

                self.about_pg.update_content()
                self.canvas.controls = [self.about_pg]
                log.info("Página 'ABOUT' actualizada.")

            case ContentStyle.ADMIN:
                if not isinstance(self.admin_pg, AdminPage):
                    self.admin_pg = AdminPage(self.page, self.snackbar, self.__confirm_changes)
                    self.canvas.controls = [self.admin_pg]
                    log.info("Página 'ADMIN' creada.")

                self.admin_pg.update_content()
                self.canvas.controls = [self.admin_pg]
                log.info("Página 'ADMIN' actualizada.")

            case ContentStyle.CREDITCARDS:
                if not isinstance(self.creditcard_pg, CreditcCardsPage):
                    self.creditcard_pg = CreditcCardsPage(self.page, self.snackbar, self.__confirm_changes)
                    self.canvas.controls = [self.creditcard_pg]
                    log.info("Página 'CREDITCARDS' creada.")

                self.creditcard_pg.update_content()
                self.canvas.controls = [self.creditcard_pg]
                log.info("Página 'CREDITCARDS' actualizada.")

            case ContentStyle.EMPTY:
                self.buttons.controls.clear()
                self.canvas.controls.clear()

            case ContentStyle.ENTRIES:
                if not isinstance(self.entries_pg, EntriesPage):
                    self.entries_pg = EntriesPage(self.page, self.snackbar, self.__confirm_changes)
                    self.canvas.controls = [self.entries_pg]
                    log.info("Página 'ENTRIES' creada.")

                self.entries_pg.get_user_input(user_input)
                self.entries_pg.update_content()
                self.canvas.controls = [self.entries_pg]
                log.info("Página 'ENTRIES' actualizada.")

            case ContentStyle.HOME:
                if not isinstance(self.home_pg, HomePage):
                    self.home_pg = HomePage(self.page, self.snackbar, self.__confirm_changes)
                    self.canvas.controls = [self.home_pg]
                    log.info("Página 'HOME' creada.")

                self.home_pg.update_content()
                self.canvas.controls = [self.home_pg]
                log.info("Página 'HOME' actualizada.")

            case ContentStyle.NOTES:
                if not isinstance(self.note_pg, NotesPage):
                    self.note_pg = NotesPage(self.page, self.snackbar, self.__confirm_changes)
                    self.canvas.controls = [self.note_pg]
                    log.info("Página 'NOTES' creada.")

                self.note_pg.update_content()
                self.canvas.controls = [self.note_pg]
                log.info("Página 'NOTES' actualizada.")

            case ContentStyle.SETTINGS:
                if not isinstance(self.settings_pg, SettingsPage):
                    self.settings_pg = SettingsPage(self.page, self.snackbar)
                    self.canvas.controls = [self.settings_pg]
                    log.info("Página 'SETTINGS' creada.")

                self.settings_pg.update_content()
                self.canvas.controls = [self.settings_pg]
                log.info("Página 'SETTINGS' actualizada.")

            case ContentStyle.SITES:
                if not isinstance(self.sites_pg, SitesPage):
                    self.sites_pg = SitesPage(self.page, self.snackbar, self.__confirm_changes)
                    self.canvas.controls = [self.sites_pg]
                    log.info("Página 'SITES' creada.")

                self.sites_pg.update_content()
                self.canvas.controls = [self.sites_pg]
                log.info("Página 'SITES' actualizada.")

    def change_content(self, title: str, style: ContentStyle, buttons: list[ft.Control] | None = None) -> None:
        self.style = style
        self.title.value = title
        self.buttons.controls = buttons
        self.__update_appearance()

    def show_results(self, user_input: str) -> None:
        self.style = ContentStyle.ENTRIES
        self.title.value = f"Buscando '{user_input}'..."
        self.buttons.controls.clear()
        self.__update_appearance(user_input)

    def __confirm_changes(self) -> None:
        self.__update_appearance()
        self.update()
