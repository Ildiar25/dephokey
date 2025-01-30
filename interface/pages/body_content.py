import flet as ft
from typing import List


from shared.utils.colors import *


class BodyContent(ft.Column):
    def __init__(self, title: str = "", buttons: List[ft.Control] | None = None,
                 widgets: List[ft.Control] | None = None, visible: bool = True) -> None:
        super().__init__()

        # Main elements
        self.title = ft.Text(
            title,
            font_family="AlbertSansB", color=primaryTextColor, size=24
        )
        self.buttons = ft.Row(
            controls=buttons
        )

        # Body design
        self.spacing = 32
        self.visible = visible
        self.scroll = ft.ScrollMode.AUTO
        self.expand = True

        # Body content
        self.controls = [
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[self.title, self.buttons]
            ),
            ft.Row(
                expand=True,
                wrap=True,
                spacing=16,
                controls=widgets
            )
        ]
