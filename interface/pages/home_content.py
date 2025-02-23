import flet as ft
from typing import Callable

from data.db_orm import session

from features.models.user import User
from features.models import Site, CreditCard, Note

from interface.controls import Snackbar
from interface.pages.widgets import *


class HomePage(ft.Row):
    def __init__(self, page: ft.Page, snackbar: Snackbar, update_changes: Callable[[], None]) -> None:
        super().__init__()

        # General attributes
        self.page = page
        self.snackbar = snackbar
        self.update_changes = update_changes
        self.limiter = 2

        # Home attributes
        self.user: User = self.page.session.get("session")
        self.sites = session.query(Site).filter_by(
            user_id=self.user.id).order_by(Site.created.desc()).limit(self.limiter).all()
        self.creditcards = session.query(CreditCard).filter_by(
            user_id=self.user.id).order_by(CreditCard.created.desc()).limit(self.limiter).all()
        self.notes = session.query(Note).filter_by(
            user_id=self.user.id).order_by(Note.created.desc()).limit(self.limiter).all()

        # Design settings
        self.spacing = 48
        self.alignment = ft.MainAxisAlignment.SPACE_AROUND
        self.vertical_alignment = ft.CrossAxisAlignment.START

        self.controls = [
            ft.Column(
                width=355,
                alignment=ft.MainAxisAlignment.START,
                spacing=16,
                controls=[
                    ft.Text(value="Nuevas direcciones web", font_family="AlbertSansR", size=20)
                ]
            ),
            ft.Column(
                width=355,
                alignment=ft.MainAxisAlignment.START,
                spacing=16,
                controls=[
                    ft.Text(value="Nuevas tarjetas", font_family="AlbertSansR", size=20),
                ]
            ),
            ft.Column(
                width=355,
                alignment=ft.MainAxisAlignment.START,
                spacing=16,
                controls=[
                    ft.Text(value="Nuevas notas", font_family="AlbertSansR", size=20),
                ]
            ),
            ft.Column(
                width=355,
                alignment=ft.MainAxisAlignment.START,
                spacing=16,
                controls=[

                ]
            )
        ]

        self.__update_lists()

    def __update_lists(self) -> None:
        for site in self.sites:
            self.controls[0].controls.append(SiteWidget(site, self.page, self.update_changes))
        for creditcard in self.creditcards:
            self.controls[1].controls.append(CreditCardWidget(creditcard, self.page, self.update_changes))
        for note in self.notes:
            self.controls[2].controls.append(NoteWidget(note, self.page, self.update_changes))
