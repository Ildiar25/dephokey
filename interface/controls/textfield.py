import flet as ft
from typing import Callable

from shared.utils.colors import *


class CustomTextField(ft.TextField):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        # Text design settings
        self.cursor_color = cursorTextfieldColor
        self.selection_color = selectCursorTextfieldColor
        self.label_style = ft.TextStyle(
            color=labelTextfieldColor
        )

        # Field design settings
        self.border_radius = 4
        self.border_color = staticBorderTextfieldColor
        self.focused_border_color = selectedBorderTextfieldColor
