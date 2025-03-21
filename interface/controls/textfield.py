import flet as ft

from shared.utils.colors import (
    neutral20,
    primaryCorporateColor,
    secondaryTextColor,
)


class CustomTextField(ft.TextField):
    """Creates a custom text field."""
    def __init__(self, error: str | None = None, **kwargs) -> None:
        super().__init__(**kwargs)

        # Specific settings
        self.error_text = error

        # Text design settings
        self.cursor_color = primaryCorporateColor
        self.selection_color = secondaryTextColor
        self.label_style = ft.TextStyle(color=secondaryTextColor)
        self.hint_style = ft.TextStyle(color=secondaryTextColor)

        # Field design settings
        self.border_radius = 4
        self.border_color = neutral20
        self.focused_border_color = primaryCorporateColor

    def reset_error(self) -> None:
        self.error_text = None
        self.update()

    def show_error(self, msg: str) -> None:
        self.error_text = msg
        self.update()
