import flet as ft
from typing import Callable

from shared.utils.colors import *


class CustomTextField(ft.TextField):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        # Text design settings
        self.cursor_color = cursorColorFieldText
        self.selection_color = selectionColorFieldText
        self.label_style = ft.TextStyle(
            color=labelTextFieldColor
        )

        # Field design settings
        self.border_radius = 0
        self.border_color = staticBorderColorField
        self.focused_border_color = selectedBorderColorField
