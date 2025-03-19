import flet as ft

from shared.utils.colors import primaryCorporateColor, tertiaryTextColor


class Footer(ft.BottomAppBar):

    def __init__(self) -> None:
        super().__init__()

        # General settings
        self.visible = False
        self.height = 48
        self.padding = ft.padding.symmetric(vertical=16, horizontal=24)

        # Design settings
        self.bgcolor = primaryCorporateColor

        # Content
        self.content = ft.Row(
            controls=[
                ft.Text("DephoKey © 2025 · Todos los derechos reservados", color=tertiaryTextColor)
            ]
        )
