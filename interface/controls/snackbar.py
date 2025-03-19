from enum import Enum

import flet as ft

from shared.utils.colors import (
    dangerTextColor,
    infoTextColor,
    neutralDangerLight,
    neutralSuccessLight,
    neutralWarningLight,
    primaryCorporate25,
    successTextColor,
    warningTextColor,
)


class SnackbarStyle(Enum):
    INFO = "info"
    WARNING = "warning"
    DANGER = "danger"
    SUCCESS = "success"
    RESET = "reset"


class Snackbar(ft.SnackBar):
    def __init__(self, content: str = "", style: SnackbarStyle = SnackbarStyle.RESET) -> None:
        super().__init__(ft.Text(content, text_align=ft.TextAlign.CENTER))

        # Sets style & Update
        self.style = style
        self.__update_appearance()

    def change_style(self, msg: str, style: SnackbarStyle) -> None:
        self.content.value = msg
        self.style = style
        self.__update_appearance()

    def __update_appearance(self) -> None:
        match self.style:
            case SnackbarStyle.INFO:
                self.bgcolor = primaryCorporate25
                self.content.color = infoTextColor
                self.open = True

            case SnackbarStyle.WARNING:
                self.bgcolor = neutralWarningLight
                self.content.color = warningTextColor
                self.open = True

            case SnackbarStyle.DANGER:
                self.bgcolor = neutralDangerLight
                self.content.color = dangerTextColor
                self.open = True

            case SnackbarStyle.SUCCESS:
                self.bgcolor = neutralSuccessLight
                self.content.color = successTextColor
                self.open = True

            case SnackbarStyle.RESET:
                self.bgcolor = None
                self.content.value = ""
                self.open = False
