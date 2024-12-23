import flet as ft

from shared.utils.colors import *


class CustomCheckbox(ft.Checkbox):
    def __init__(self, label: str) -> None:
        super().__init__()

        # Specific settings
        self.label = label

        # Design settings
        self.shape = ft.CircleBorder()
        self.fill_color = {
            ft.ControlState.DEFAULT: defaultFillCheckboxColor,
            ft.ControlState.SELECTED: selectedFillCheckboxColor
        }
        self.hover_color = transparentColor
        self.border_side = {
            ft.ControlState.HOVERED: ft.BorderSide(2, selectedBorderCheckboxColor, 0),
            ft.ControlState.FOCUSED: ft.BorderSide(2, selectedBorderCheckboxColor, 0),
        }
