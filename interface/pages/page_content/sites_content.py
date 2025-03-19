from collections.abc import Callable

import flet as ft

from data.db_orm import session
from features.models import Site
from features.models.user import User
from interface.controls.snackbar import Snackbar
from interface.pages.widgets import SiteWidget


class SitesPage(ft.Column):
    def __init__(self, page: ft.Page, snackbar: Snackbar, update_changes: Callable[[], None]) -> None:
        super().__init__()

        # General attributes
        self.page = page
        self.snackbar = snackbar
        self.update_changes = update_changes

        # SitesPage attributes
        self.user: User = self.page.session.get("session")
        self.sites = []

        # Body content
        self.sites_row = ft.Row(wrap=True, spacing=16)
        self.controls = [self.sites_row]

        self.update_content()

    def update_content(self) -> None:
        self.sites = session.query(Site).filter_by(user_id=self.user.id).all()
        self.__populate_row(self.sites)

    def __populate_row(self, sites: list[Site]) -> None:
        self.sites_row.controls.clear()
        for site in sites:
            self.sites_row.controls.append(SiteWidget(site, self.page, self.update_changes))
