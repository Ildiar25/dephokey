from collections.abc import Callable

import flet as ft

from data.db_orm import session
from features.models import CreditCard, Note, Site
from features.models.user import User
from interface.controls.snackbar import Snackbar
from interface.pages.widgets import CreditCardWidget, NoteWidget, SiteWidget


class HomePage(ft.Row):
    """Displays the newest elements added."""
    def __init__(self, page: ft.Page, snackbar: Snackbar, update_changes: Callable[[], None]) -> None:
        super().__init__()

        # General attributes
        self.page = page
        self.snackbar = snackbar
        self.update_changes = update_changes
        self.limiter = 2

        # Home attributes
        self.user: User = self.page.session.get("session")
        self.sites = []
        self.creditcards = []
        self.notes = []

        # Body content
        self.sites_column = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.START
        )
        self.creditcards_column = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.START
        )
        self.notes_column = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.START
        )

        # Settings design
        self.alignment = ft.MainAxisAlignment.SPACE_AROUND
        self.vertical_alignment = ft.CrossAxisAlignment.START
        self.scroll = ft.ScrollMode.AUTO

        self.controls = [
            ft.Column(
                width=400,
                alignment=ft.MainAxisAlignment.START,
                spacing=16,
                controls=[
                    ft.Text(value="Nuevas direcciones web", font_family="AlbertSansR", size=20),
                    self.sites_column,
                ]
            ),
            ft.Column(
                width=400,
                alignment=ft.MainAxisAlignment.START,
                spacing=16,
                controls=[
                    ft.Text(value="Nuevas tarjetas", font_family="AlbertSansR", size=20),
                    self.creditcards_column,
                ]
            ),
            ft.Column(
                width=400,
                alignment=ft.MainAxisAlignment.START,
                spacing=16,
                controls=[
                    ft.Text(value="Nuevas notas", font_family="AlbertSansR", size=20),
                    self.notes_column,
                ]
            ),
            ft.Column(
                width=400, alignment=ft.MainAxisAlignment.START, controls=[]
            ),
        ]

        self.update_content()

    def __populate_columns(self, sites: list[Site], creditcards: list[CreditCard], notes: list[Note]) -> None:
        self.__clear_columns()
        for site in sites:
            self.sites_column.controls.append(SiteWidget(site, self.page, self.update_changes))
        for creditcard in creditcards:
            self.creditcards_column.controls.append(CreditCardWidget(creditcard, self.page, self.update_changes))
        for note in notes:
            self.notes_column.controls.append(NoteWidget(note, self.page, self.update_changes))

    def __clear_columns(self) -> None:
        self.sites_column.controls.clear()
        self.creditcards_column.controls.clear()
        self.notes_column.controls.clear()

    def update_content(self) -> None:
        self.sites = session.query(Site).filter_by(
            user_id=self.user.id
        ).order_by(
            Site.created.desc()
        ).limit(self.limiter).all()

        self.creditcards = session.query(CreditCard).filter_by(
            user_id=self.user.id
        ).order_by(
            CreditCard.created.desc()
        ).limit(self.limiter).all()

        self.notes = session.query(Note).filter_by(
            user_id=self.user.id
        ).order_by(
            Note.created.desc()
        ).limit(self.limiter).all()

        self.__populate_columns(self.sites, self.creditcards, self.notes)
