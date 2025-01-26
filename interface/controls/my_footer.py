import flet as ft

from shared.utils.colors import *


class Footer(ft.BottomAppBar):

    def __init__(self) -> None:
        super().__init__()

        # General settings
        self.visible = False
        self.height = 48
        self.padding = ft.padding.only(24, 16, 24, 16)

        # Design settings
        self.bgcolor = bgFooterColor

        # Content
        self.content = ft.Row(
            controls=[
                ft.Text("DephoKey © 2025 · Todos los derechos reservados", color=textFooterColor)
            ]
        )