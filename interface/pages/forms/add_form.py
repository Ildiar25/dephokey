import flet as ft
from enum import Enum

from interface.controls import CustomElevatedButton

from shared.utils.colors import *


class AddFormStyle(Enum):
    CREDITCARD = "creditcard"
    NOTE = "note"
    SITE = "site"


class AddForm(ft.AlertDialog):
    def __init__(self, page: ft.Page, ) -> None:
        super().__init__()
