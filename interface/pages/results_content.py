import flet as ft
from typing import Callable, List, Type

from data.db_orm import session

from features.models.user import User
from features.models import Site, CreditCard, Note

from interface.controls import Snackbar

from interface.pages.widgets import SiteWidget, CreditCardWidget, NoteWidget


class ResultsPage(ft.Column):
    def __init__(self, page: ft.Page, snackbar: Snackbar, update_changes: Callable[[], None]) -> None:
        super().__init__()

        # General attributes
        self.page = page
        self.snackbar = snackbar
        self.update_changes = update_changes

        # Body design
        self.spacing = 24

        # Body content
        self.sites_row = ft.Row(scroll=ft.ScrollMode.AUTO, vertical_alignment=ft.CrossAxisAlignment.START)
        self.creditcards_row = ft.Row(scroll=ft.ScrollMode.AUTO, vertical_alignment=ft.CrossAxisAlignment.START)
        self.notes_row = ft.Row(scroll=ft.ScrollMode.AUTO, vertical_alignment=ft.CrossAxisAlignment.START)

        self.controls = [
            ft.Text("Sitios encontrados:"),
            self.sites_row,
            ft.Text("Tarjetas encontradas:"),
            self.creditcards_row,
            ft.Text("Notas encontradas:"),
            self.notes_row
        ]

        self.update_results("")

    def update_results(self, user_input: str):
        # Update searchbar results and show it
        results = user_input.strip()
        user: User = self.page.session.get("session")

        ss = session.query(Site).filter_by(user_id=user.id).filter(Site.address.like(f"%{results}%")).all()
        cs = session.query(CreditCard).filter_by(user_id=user.id).filter(CreditCard.alias.like(f"%{results}%")).all()
        ns = session.query(Note).filter_by(user_id=user.id).filter(Note.title.like(f"%{results}%")).all()

        self.__populate_rows(ss, self.sites_row, SiteWidget)
        self.__populate_rows(cs, self.creditcards_row, CreditCardWidget)
        self.__populate_rows(ns, self.notes_row, NoteWidget)

    def __populate_rows(self, results: List[Site | CreditCard | Note],
                        row: ft.Row, widget: Type[SiteWidget | CreditCardWidget | NoteWidget]) -> None:
        row.controls.clear()
        if len(results) != 0:
            for item in results:
                row.controls.append(widget(item, self.page, self.update_changes))
        else:
            row.controls.append(ft.Text("Ningún elemento encontrado."))
