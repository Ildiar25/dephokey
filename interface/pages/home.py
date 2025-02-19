import flet as ft

from data.db_orm import session

from features.models.user import UserRole,User
from features.models import *

from interface.pages.body_content import BodyContent
from interface.pages.admin import Admin
from interface.controls import CustomAppbar, CustomSidebar

from shared.utils.colors import *


class Home(ft.Container):
    def __init__(self, page: ft.Page) -> None:
        super().__init__()

        # General attributes
        self.page = page
        self.user: User = self.page.session.get("session")
        self.snackbar = ft.SnackBar(
            bgcolor=bgSnackbarDangerColor,
            content=ft.Text(
                "",
                text_align=ft.TextAlign.CENTER,
                color=dangerTextColor
            )
        )

        # General content
        self.admin_page = Admin(self.page)
        if self.user.role == UserRole.ADMIN:
            self.body_content = BodyContent(
                title="Bienvenido Administrador!",
                widgets=[self.admin_page]
            )

        else:
            self.body_content = BodyContent(
                title=f"Bienvenido/a {self.user.fullname.split(' ')[0]}!",
                widgets=[]
            )

        # Sidebar controller & Searchbar function
        self.sidebar = CustomSidebar(self.page, self.body_content)
        self.page.appbar = CustomAppbar(
            self.page, self.body_content, self.snackbar, self.admin_page,
            search_bar=True if self.user.role == UserRole.CLIENT else False,
            find_function=self.find_elements if self.user.role == UserRole.CLIENT else None)


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

        self.sidebar_location.visible = True if self.user.role == UserRole.CLIENT else False

        # Page design
        self.expand = True
        self.page.bgcolor = neutral05
        self.page.appbar.visible = True
        self.page.bottom_appbar.visible = True

        # Dashboard
        self.active_content = ft.Container(
            expand=True,
            padding=ft.padding.only(56, 56, 56, 28),
            content=ft.Stack(
                controls=[
                    ft.Container(image=ft.DecorationImage("interface/assets/bgimage-home-page.png", fit=ft.ImageFit.COVER)),
                    self.body_content
                ]
            )
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
                        self.sidebar_location, self.active_content, self.snackbar
                    ]
                )
            ]
        )

    def find_elements(self, e: ft.ControlEvent) -> None:
        self.body_content.controls[0].controls[0].value = f"Buscando {e.control.value.title()}"
        self.body_content.controls[0].controls[1].controls = []
        self.body_content.update()
