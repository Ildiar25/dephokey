import flet as ft

from shared.utils.colors import *


class CustomFloatingButton(ft.FloatingActionButton):
    def __init__(self) -> None:
        super().__init__()

        # Design settings
        self.shape = ft.CircleBorder()
        self.bgcolor = bgFloatingButtonColor
        self.focus_color = ft.Colors.with_opacity(0.3, focusFloatingButtonColor)
        self.hover_elevation = 16

        self.icon = ft.Icons.ADD_CIRCLE_ROUNDED
        self.foreground_color = fgFloatingButtonColor

        self.visible = False



