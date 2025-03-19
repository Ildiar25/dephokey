from collections.abc import Callable

import flet as ft


class CustomSearchBar(ft.Container):
    def __init__(self, width: int, function: Callable[[ft.ControlEvent], None]) -> None:
        super().__init__()

        # Specific settings
        self.width = width
        self.function = function
        self.textfield_on_focus = False
        self.textfield = ft.TextField(
            expand=True,
            border_color=ft.Colors.TRANSPARENT,
            height=20,
            text_size=14,
            content_padding=0,
            cursor_color=ft.Colors.BLACK,
            cursor_width=1,
            color=ft.Colors.BLACK,
            hint_text="Buscar",
            on_change=self.__text_changed,
            on_focus=self.__is_focused,
            on_blur=self.__is_focused,
            max_length=100
        )

        # Container design
        self.bgcolor = ft.Colors.WHITE
        self.border_radius = 6
        self.padding = 8
        self.opacity = 0.4

        # Animation
        self.animate_opacity = 250

        # Container content
        self.content = ft.Row(
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Icon(ft.Icons.SEARCH_ROUNDED, size=17, color=ft.Colors.BLACK, opacity=0.85),
                self.textfield
            ]
        )

    def __text_changed(self, event: ft.ControlEvent) -> None:
        self.function(event)
        self.update()

    def __is_focused(self, _: ft.ControlEvent) -> None:
        self.textfield_on_focus = not self.textfield_on_focus
        if self.textfield_on_focus or self.textfield.value:
            self.opacity = 1
        else:
            self.opacity = 0.4
        self.update()
