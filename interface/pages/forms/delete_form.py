import flet as ft
from typing import Union, Callable

from interface.controls import CustomElevatedButton

from features.models.user import User
from features.models import *

from shared.utils.colors import *


class DeleteForm(ft.AlertDialog):
    def __init__(self, page: ft.Page, element: Union[CreditCard, Site, Note, User, PasswordRequest],
                 delete_fun: Callable[[ft.ControlEvent], None]) -> None:
        super().__init__()

        # General attributes
        self.page = page
        self.element = element
        self.delete_fun = delete_fun
        self.element_type = type(self.element).__name__

        match self.element_type:
            case "Site":
                self.element_type = "sitio web"
            case "Note":
                self.element_type = "nota segura"
            case "CreditCard":
                self.element_type = "tarjeta de crédito"
            case "User":
                self.element_type = "usuario"
            case "PasswordRequest":
                self.element_type = "reseteo de contraseña"
            case _:
                pass

        # Form settings
        self.modal = True

        # Form content
        self.title = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text(
                    f"Eliminar {self.element_type}",
                    font_family="AlbertSansB",
                    size=20
                ),
                ft.IconButton(
                    ft.Icons.CLOSE_ROUNDED,
                    icon_color=iconDeleteFormColor,
                    on_click=lambda _: self.page.close(self),
                    highlight_color=selectedIconDeleteFormColor,
                    hover_color=hoverIconDeleteFormColor
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

    def delete(self, e: ft.ControlEvent) -> None:
        self.delete_fun(e)
        self.page.close(self)
