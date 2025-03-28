from collections.abc import Callable

import flet as ft

from data.db_orm import session
from features.models import CreditCard
from features.models.user import User
from interface.controls.snackbar import Snackbar
from interface.pages.widgets import CreditCardWidget


class CreditcCardsPage(ft.Column):
    """Displays all creditcards and update interface."""
    def __init__(self, page: ft.Page, snackbar: Snackbar, update_changes: Callable[[], None]) -> None:
        super().__init__()

        # General attributes
        self.page = page
        self.snackbar = snackbar
        self.update_changes = update_changes

        # CreditCardsPage attributes
        self.user: User = self.page.session.get("session")
        self.creditcards = []

        # Body content
        self.creditcards_row = ft.Row(wrap=True, spacing=16)
        self.controls = [self.creditcards_row]

        self.update_content()

    def update_content(self) -> None:
        self.creditcards = session.query(CreditCard).filter_by(user_id=self.user.id).all()
        self.__populate_row(self.creditcards)

    def __populate_row(self, creditcards: list[CreditCard]) -> None:
        self.creditcards_row.controls.clear()
        for creditcard in creditcards:
            self.creditcards_row.controls.append(CreditCardWidget(creditcard, self.page, self.update_changes))
