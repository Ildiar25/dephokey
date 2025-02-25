import flet as ft
from typing import Callable

from interface.controls import Snackbar


class AboutPage(ft.Column):
    def __init__(self, page: ft.Page, snackbar: Snackbar, update_changes: Callable[[], None]) -> None:
        super().__init__()

        # General attributes
        self.page = page
        self.snackbar = snackbar
        self.update_changes = update_changes

        self.update_content()

    def update_content(self) -> None:
        pass
