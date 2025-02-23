import flet as ft
from typing import Callable

from data.db_orm import session

from features.models.user import User
from features.models import Site, CreditCard, Note

from interface.controls import Snackbar


class ResultsPage(ft.Row):
    def __init__(self, page: ft.Page, snackbar: Snackbar, update_changes: Callable[[], None], user_input: str) -> None:
        super().__init__()

        # General attributes
        self.page = page
        self.snackbar = snackbar
        self.update_changes = update_changes
        self.user_input = user_input.strip()

        # Results attributes
        self.user: User = self.page.session.get("session")
        self.sites = session.query(Site).filter_by(
            user_id=self.user.id).filter(Site.address.like(f"%{self.user_input}%")).all()
        self.creditcards = session.query(CreditCard).filter_by(
            user_id=self.user.id).filter(CreditCard.alias.like(f"%{self.user_input}%")).all()
        self.notes = session.query(Note).filter_by(
            user_id=self.user.id).filter(Note.title.like(f"%{self.user_input}%")).all()


        # Body design
        self.spacing = 24

        # Body content
        self.controls = [
            ft.Text("Hola")
        ]







