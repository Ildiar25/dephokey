from collections.abc import Callable

import flet as ft

from data.db_orm import session
from features.models import CreditCard, Note, Site
from interface.controls.snackbar import Snackbar
from interface.pages.widgets import CreditCardWidget, NoteWidget, SiteWidget
from shared.utils.colors import primaryCorporateColor, primaryTextColor


class EntriesPage(ft.Column):
    """Displays all elements matched with user entry."""
    def __init__(self, page: ft.Page, snackbar: Snackbar, update_changes: Callable[[], None]) -> None:
        super().__init__()

        # General attributes
        self.page = page
        self.snackbar = snackbar
        self.update_changes = update_changes
        self.user_input = ""

        # Entry attributes
        self.user = self.page.session.get("session")
        self.sites = []
        self.creditcards = []
        self.notes = []

        # Body design
        self.spacing = 24

        # Entry rows
        self.sites_found = ft.Row(
            scroll=ft.ScrollMode.AUTO,
            vertical_alignment=ft.CrossAxisAlignment.START,
            height=210
        )
        self.creditcards_found = ft.Row(
            scroll=ft.ScrollMode.AUTO,
            vertical_alignment=ft.CrossAxisAlignment.START,
            height=235
        )
        self.notes_found = ft.Row(
            scroll=ft.ScrollMode.AUTO,
            vertical_alignment=ft.CrossAxisAlignment.START,
            height=320
        )

        # Body Content
        self.controls = [
            ft.Text(
                value=" ⳾ Sitios encontrados:",
                font_family="AlbertSansB",
                color=primaryTextColor,
                size=16
            ),
            self.sites_found,
            ft.Divider(thickness=2, color=primaryCorporateColor, height=6),
            ft.Text(
                value=" ⳾ Tarjetas encontradas:",
                font_family="AlbertSansB",
                color=primaryTextColor,
                size=16
            ),
            self.creditcards_found,
            ft.Divider(thickness=2, color=primaryCorporateColor, height=6),
            ft.Text(
                value=" ⳾ Notas encontradas:",
                font_family="AlbertSansB",
                color=primaryTextColor,
                size=16
            ),
            self.notes_found,
        ]

        self.update_content()

    def get_user_input(self, user_input: str) -> None:
        self.user_input = user_input if user_input is not None else self.user_input
        self.update_content()

    def __populate_rows(self, sites: list[Site], creditcards: list[CreditCard], notes: list[Note]) -> None:
        self.__clear_rows()
        for site in sites:
            self.sites_found.controls.append(SiteWidget(site, self.page, self.update_changes))
        for creditcard in creditcards:
            self.creditcards_found.controls.append(CreditCardWidget(creditcard, self.page, self.update_changes))
        for note in notes:
            self.notes_found.controls.append(NoteWidget(note, self.page, self.update_changes))

    def __clear_rows(self) -> None:
        self.sites_found.controls.clear()
        self.creditcards_found.controls.clear()
        self.notes_found.controls.clear()

    def update_content(self) -> None:
        self.sites = session.query(Site).filter_by(
            user_id=self.user.id
        ).filter(
            Site.name.like(f"%{self.user_input}%")
        ).all()

        self.creditcards = session.query(CreditCard).filter_by(
            user_id=self.user.id
        ).filter(
            CreditCard.alias.like(f"%{self.user_input}%")
        ).all()

        self.notes = session.query(Note).filter_by(
            user_id=self.user.id
        ).filter(
            Note.title.like(f"%{self.user_input}%")
        ).all()

        if self.user_input == "":
            self.sites = []
            self.creditcards = []
            self.notes = []

        self.__populate_rows(self.sites, self.creditcards, self.notes)
