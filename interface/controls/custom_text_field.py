import flet as ft

from shared.utils.colors import *


class CustomTextField(ft.TextField):
    def __init__(self, label: str, password: bool | None = None, can_reveal_password: bool | None = None,
                 autofocus: bool | None = None) -> None:
        super().__init__()

        # Specific settings
        self.label = label
        self.password = password
        self.can_reveal_password = can_reveal_password
        self.autofocus = autofocus

        # Text design settings
        self.cursor_color = cursorColorFieldText
        self.selection_color = selectionColorFieldText
        self.label_style = ft.TextStyle(
            color=labelTextColor
        )

        # Field design settings
        self.border_radius = 0
        self.border_color = staticBorderColorField
        self.focused_border_color = selectedBorderColorField
