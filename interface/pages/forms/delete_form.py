import flet as ft
from enum import Enum
from typing import Callable

from .base_form import BaseForm
from interface.controls import CustomElevatedButton, ButtonStyle

from shared.utils.colors import *


class DeleteFormStyle(Enum):
    CREDITCARD = "creditcard"
    NOTE = "note"
    PASS_REQ = "pass_req"
    SITE = "site"
    USER = "user"


class DeleteForm(BaseForm):
    def __init__(self, page: ft.Page, delete_function: Callable[[ft.ControlEvent], None],
                 style: DeleteFormStyle) -> None:
        super().__init__()

        # TODO: Implementar eliminación de eleemntos en el propio formulario. Tener en cuenta la actualización de las
        #  vistas de elementos (content_manager)

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
                value="¿Desea eliminar este registro? Esta acción ",
                font_family="AlbertSansL",
                size=16,
                spans=[
                    ft.TextSpan(text="no se puede deshacer.", style=ft.TextStyle(font_family="AlbertSansB"))
                ]
            )
        )
        self.actions = [
            CustomElevatedButton(name="Cancelar", style=ButtonStyle.CANCEL, on_click=lambda _: self.page.close(self)),
            CustomElevatedButton(name="Eliminar", style=ButtonStyle.DELETE, on_click=self.delete)
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

        return title

    def delete(self, e: ft.ControlEvent) -> None:
        self.delete_function(e)
        self.page.close(self)
