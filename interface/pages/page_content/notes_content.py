import flet as ft
from typing import Callable, List

from data.db_orm import session

from features.models.user import User
from features.models import Note

from interface.controls import Snackbar
from interface.pages.widgets import NoteWidget


class NotesPage(ft.Column):
    def __init__(self, page: ft.Page, snackbar: Snackbar, update_changes: Callable[[], None]) -> None:
        super().__init__()

        # General attributes
        self.page = page
        self.snackbar = snackbar
        self.update_changes = update_changes

        # NotesPage attributes
        self.user: User = self.page.session.get("session")
        self.notes = []

        # Body content
        self.notes_row = ft.Row(wrap=True, spacing=16)
        self.controls = [self.notes_row]

        self.update_content()

    def update_content(self) -> None:
        self.notes = session.query(Note).filter_by(user_id=self.user.id).all()
        self.__populate_row(self.notes)

    def __populate_row(self, notes: List[Note]) -> None:
        self.notes_row.controls.clear()
        for note in notes:
            self.notes_row.controls.append(NoteWidget(note, self.page, self.update_changes))
