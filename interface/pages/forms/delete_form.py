import flet as ft
from enum import Enum
from typing import Callable

from interface.controls import CustomElevatedButton

from shared.utils.colors import *


class DeleteFormStyle(Enum):
    CREDITCARD = "creditcard"
    NOTE = "note"
    PASS_REQ = "pass_req"
    SITE = "site"
    USER = "user"


class DeleteForm(ft.AlertDialog):
    def __init__(self, page: ft.Page, delete_function: Callable[[ft.ControlEvent], None],
                 style: DeleteFormStyle) -> None:
        super().__init__()

        # General attributes
        self.page = page
        self.delete_function = delete_function
        self.text_title = self.__update_form_title(style)

        # Form settings
        self.modal = True

        # Form content
        self.title = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text(
                    value=f"Eliminar {self.text_title}",
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
                value="¿Desea eliminar este registro? Esta acción no se puede deshacer.",
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

    @staticmethod
    def __update_form_title(style: DeleteFormStyle) -> str:
        title = ""

        match style:
            case DeleteFormStyle.CREDITCARD:
                title = "tarjeta de crédito"
            case DeleteFormStyle.NOTE:
                title = "nota segura"
            case DeleteFormStyle.PASS_REQ:
                title = "registro de cambio"
            case DeleteFormStyle.SITE:
                title = "sitio"
            case DeleteFormStyle.USER:
                title = "usuario"
            case _:
                pass

        return title

    def delete(self, e: ft.ControlEvent) -> None:
        self.delete_function(e)
        self.page.close(self)
