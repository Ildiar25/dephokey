import flet as ft

from data.db_orm import session

from features.models.user import UserRole
from features.models import *

from interface.pages.body_content import BodyContent
from interface.controls import CustomAppbar, CustomSidebar

from shared.utils.colors import *


class Home(ft.Container):
    def __init__(self, page: ft.Page) -> None:
        super().__init__()

        # General attributes
        self.page = page
        self.role = self.page.session.get("session").role

        # General content
        self.body_content = BodyContent()

        # Sidebar controller & Searchbar function
        self.page.appbar = CustomAppbar(self.body_content, search_bar=True, find_function=self.find_elements)
        self.sidebar = CustomSidebar(self.page, self.body_content)
        # self.sidebar_location = ft.Row(controls=[self.sidebar])

        self.sidebar_location = ft.Row(
            width=200,
            controls=[
                ft.Container(
                    expand=True,
                    height=1000,
                    bgcolor=bgSidebarColor,
                    content=self.sidebar
                )
            ]
        )

        self.sidebar_location.visible = True if self.role == UserRole.CLIENT else False

        # Page design
        self.expand = True
        self.page.bgcolor = neutral05
        self.page.appbar.visible = True
        self.page.bottom_appbar.visible = True

        # Dashboard
        self.active_content = ft.Container(
            expand=True,
            padding=ft.padding.only(56, 57, 56, 57),
            content=self.body_content
        )
        self.content = ft.Column(
            expand=True,
            spacing=0,
            controls=[
                # Divider
                ft.Divider(height=1, thickness=1, color=neutral05),

                # Sidebar & Bodycontent
                ft.Row(
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    expand=True,
                    spacing=0,
                    controls=[
                        self.sidebar_location, self.active_content
                    ]
                )
            ]
        )

    def find_elements(self, e: ft.ControlEvent) -> None:
        self.body_content.controls[0].controls[0].value = f"Buscando {e.control.value}"
        self.body_content.controls[0].controls[1].controls = []
        self.body_content.update()
