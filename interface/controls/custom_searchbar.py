import flet as ft
from typing import Callable


class CustomSearchBar(ft.Container):
    def __init__(self, width: int, function: Callable[[ft.ControlEvent], None]) -> None:
        super().__init__()

        # Specific settings
        self.width = width
        self.function = function

        # Container design
        self.bgcolor = ft.Colors.WHITE
        self.border_radius = 6
        self.padding = 8
        self.opacity = 0.2

        # Animation
        self.animate_opacity = 250
        self.on_hover = self.toggle_bar_opacity

        # Container content
        self.content = ft.Row(
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Icon(ft.Icons.SEARCH_ROUNDED, size=17, color=ft.Colors.BLACK, opacity=0.85),
                ft.TextField(
                    expand=True,
                    border_color=ft.Colors.TRANSPARENT,
                    height=20,
                    text_size=14,
                    content_padding=0,
                    cursor_color=ft.Colors.BLACK,
                    cursor_width=1,
                    color=ft.Colors.BLACK,
                    hint_text="Buscar",
                    on_change=self.function
                )
            ]
        )

    def toggle_bar_opacity(self, event: ft.ControlEvent) -> None:
        self.opacity = 1 if event.data and self.opacity == 0.2 else 0.2
        self.update()
