import flet as ft

from features.models.user import User, UserRole
from interface.controls.appbar import CustomAppbar
from interface.controls.sidebar import CustomSidebar
from interface.controls.snackbar import Snackbar
from interface.pages.content_manager import ContentManager, ContentStyle
from shared.logger_setup import main_log as log
from shared.utils.colors import neutral05, neutral80


class Dashboard(ft.Container):
    """Creates Dashboard page and displays all main navigation elements"""
    def __init__(self, page: ft.Page) -> None:
        super().__init__()

        # General attributes
        self.page = page
        self.user: User = self.page.session.get("session")
        self.snackbar = Snackbar()

        # General content
        self.body_content = ContentManager(
            page=self.page,
            snackbar=self.snackbar,
            title=f"¡Hola {self.user.fullname.split(' ')[0]}!"
        )

        # Sidebar controller
        self.sidebar = CustomSidebar(
            page=self.page,
            snackbar=self.snackbar,
            content=self.body_content
        )
        self.sidebar_location = ft.Row(
            width=200,
            controls=[
                ft.Container(
                    expand=True,
                    height=4000,
                    bgcolor=neutral80,
                    content=self.sidebar
                )
            ]
        )

        # Appbar controller
        self.page.appbar = CustomAppbar(
            page=self.page,
            snackbar=self.snackbar,
            content=self.body_content
        )

        # Page design
        self.expand = True
        self.page.bgcolor = neutral05
        self.page.appbar.visible = True
        self.page.bottom_appbar.visible = True
        self.sidebar_location.visible = self.user.role == UserRole.CLIENT

        # Dashboard (Canvas)
        self.active_content = ft.Container(
            expand=True,
            padding=ft.padding.only(left=56, top=56, right=56, bottom=28),
            content=ft.Stack(
                controls=[
                    ft.Container(
                        image=ft.DecorationImage(
                            src=r"interface\assets\bgimage-home-page.png", fit=ft.ImageFit.COVER, opacity=0.5
                        )
                    ),
                    self.body_content,
                ]
            )
        )

        # Page content
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
                        self.sidebar_location, self.active_content, self.snackbar,
                    ]
                ),
            ]
        )

        if self.user.role == UserRole.ADMIN:
            self.body_content.change_content(
                title=f"Bienvenido {self.user.fullname.split(' ')[0]}!", style=ContentStyle.ADMIN
            )

        log.info("Página 'DASHBOARD' inicializada.")
