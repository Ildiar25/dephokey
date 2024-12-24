import flet as ft


class CustomAppbar(ft.AppBar):
    def __init__(self) -> None:
        super().__init__()

        # General settings
        self.visible = False
        self.toolbar_height = 60

        # Leading settings
        self.leading = ft.Icon(ft.Icons.START)
        self.leading_width = 240

        # Searchbar settings
        self.title = ft.TextField(hint_text="Buscar...")

        # Control settings
        self.actions = [
            ft.Container(
                content=ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(text="Salir", icon=ft.Icons.LOGOUT),
                        ft.PopupMenuItem(),
                        ft.PopupMenuItem(text="Opciones", icon=ft.Icons.SETTINGS),
                    ]
                )
            )
        ]
