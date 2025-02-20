import flet as ft
from enum import Enum

from shared.utils.colors import *


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
                self.bgcolor = bgSnackbarInfoColor
                self.content.color = infoTextColor
                self.open = True

            case SnackbarStyle.WARNING:
                self.bgcolor = bgSnackbarWarningColor
                self.content.color = warningTextColor
                self.open = True

            case SnackbarStyle.DANGER:
                self.bgcolor = bgSnackbarDangerColor
                self.content.color = dangerTextColor
                self.open = True

            case SnackbarStyle.SUCCESS:
                self.bgcolor = bgSnackbarSuccessColor
                self.content.color = successTextColor
                self.open = True

            case SnackbarStyle.RESET:
                self.bgcolor = None
                self.content.value = ""
                self.open = False
