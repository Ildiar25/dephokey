import flet as ft
from enum import Enum
from typing import Union, Callable

from interface.controls import CustomElevatedButton

from features.models.user import User
from features.models import *

from shared.utils.colors import *


class DeleteFormStyle(Enum):
    CREDITCARD = "creditcard"
    NOTE = "note"
    PASS_REQ = "pass_req"
    SITE = "site"
    USER = "user"


class DeleteForm(ft.AlertDialog):
    def __init__(self, page: ft.Page, delete_fun: Callable[[ft.ControlEvent], None],
                 del_style: DeleteFormStyle) -> None:
        super().__init__()

        # General attributes
        self.page = page
        self.delete_fun = delete_fun
        self.element_type = del_style

        match self.element_type:
            case DeleteFormStyle.CREDITCARD:
                self.text_title = "tarjeta de crédito"
            case DeleteFormStyle.NOTE:
                self.text_title = "nota segura"
            case DeleteFormStyle.PASS_REQ:
                self.text_title = "registro de cambio"
            case DeleteFormStyle.SITE:
                self.text_title = "sitio"
            case DeleteFormStyle.USER:
                self.text_title = "usuario"
            case _:
                self.text_title = "unknow"

        # Form settings
        self.modal = True

        # Form content
        self.title = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text(
                    f"Eliminar {self.text_title}",
                    font_family="AlbertSansB",
                    size=20
                ),
                ft.IconButton(
                    ft.Icons.CLOSE_ROUNDED,
                    icon_color=iconAccentGeneralFormColor,
                    on_click=lambda _: self.page.close(self),
                    highlight_color=selectedIconGeneralFormColor,
                    hover_color=hoverIconGeneralFormColor
                )
            ]
        )
        self.content = ft.Container(
            width=380,
            height=60,
            content=ft.Text(
            "¿Desea eliminar este registro? Esta acción no se puede deshacer.",
                font_family="AlbertSansL",
                size=16,
            )
        )
        self.actions = [
            CustomElevatedButton(
                name="Cancelar",
                width=84,
                foreground_color=secondaryTextColor,
                on_click=lambda _: self.page.close(self),
                border_size=-1
            ),
            CustomElevatedButton(
                name="Eliminar",
                width=84,
                foreground_color=tertiaryTextColor,
                bg_color=neutralDangerMedium,
                on_click=self.delete,
                border_size=-1
            )
        ]

        # Form design
        self.shape = ft.RoundedRectangleBorder(4)
        self.bgcolor = bgGeneralFormColor

    def delete(self, e: ft.ControlEvent) -> None:
        self.delete_fun(e)
        self.page.close(self)
