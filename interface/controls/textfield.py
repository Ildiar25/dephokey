import flet as ft

from shared.utils.colors import (
    cursorTextfieldColor,
    secondaryTextColor,
    selectCursorTextfieldColor,
    selectedBorderTextfieldColor,
    staticBorderTextfieldColor,
)


class CustomTextField(ft.TextField):
    def __init__(self, error: str | None = None, **kwargs) -> None:
        super().__init__(**kwargs)

        # Specific settings
        self.error_text = error

        # Text design settings
        self.cursor_color = cursorTextfieldColor
        self.selection_color = selectCursorTextfieldColor
        self.label_style = ft.TextStyle(color=secondaryTextColor)
        self.hint_style = ft.TextStyle(color=secondaryTextColor)

        # Field design settings
        self.border_radius = 4
        self.border_color = staticBorderTextfieldColor
        self.focused_border_color = selectedBorderTextfieldColor

    def reset_error(self) -> None:
        self.error_text = None
        self.update()

    def show_error(self, msg: str) -> None:
        self.error_text = msg
        self.update()
