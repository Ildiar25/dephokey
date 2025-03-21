import time
from collections.abc import Callable
from enum import Enum
from types import NoneType

import flet as ft

from data.db_orm import session
from features.models import CreditCard, Note, PasswordRequest, Site
from features.models.user import User
from interface.controls import CustomElevatedButton
from interface.controls.e_button import ButtonStyle
from interface.controls.snackbar import Snackbar
from interface.pages.loading_page import LoadingPage
from shared.utils.colors import primaryCorporate100, primaryTextColor

from .base_form import BaseForm


class DeleteFormStyle(Enum):
    USER = "user"
    SITE = "site"
    CREDITCARD = "creditcard"
    NOTE = "note"
    PASS_REQ = "pass_req"


class DeleteForm(BaseForm):
    def __init__(
            self,
            page: ft.Page,
            item: User | Site | CreditCard | Note | PasswordRequest,
            style: DeleteFormStyle,
            update_changes: Callable[[], None] | None = None,
            snackbar: Snackbar | None = None,
            update_dropdown: Callable[[], None] | None = None
    ) -> None:
        super().__init__()

        # General attributes
        self.page = page
        self.snackbar = snackbar
        self.style = style

        # Form attributes
        self.user: User = self.page.session.get("session")
        self.item = item
        self.update_changes = update_changes
        self.update_dropdown = update_dropdown

        # Form settings
        self.submit_button = CustomElevatedButton(name="Eliminar", style=ButtonStyle.DELETE, on_click=self.__delete)
        self.cancel_button.on_click = lambda _: self.page.close(self)

        # Form title
        self.title = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text(value="", font_family="AlbertSansB", size=20, color=primaryTextColor),
                self.close_button,
            ]
        )

        # Form content
        self.content = ft.Container(width=380, height=70)
        self.actions = [self.cancel_button, self.submit_button]

        self.__update_appearance()

    def __update_appearance(self) -> None:
        match self.style:
            case DeleteFormStyle.CREDITCARD:
                self.title.controls[0].value = "Eliminar tarjeta de crédito"

                # Content
                self.content.content = ft.Text(
                    value="¿Desea eliminar esta tarjeta? Esta acción ",
                    font_family="AlbertSansL",
                    size=16,
                    spans=[
                        ft.TextSpan(text="no se puede deshacer.", style=ft.TextStyle(font_family="AlbertSansB")),
                    ]
                )

            case DeleteFormStyle.NOTE:
                self.title.controls[0].value = "Eliminar nota segura"

                # Content
                self.content.content = ft.Text(
                    value="¿Desea eliminar esta nota? Esta acción ",
                    font_family="AlbertSansL",
                    size=16,
                    spans=[
                        ft.TextSpan(text="no se puede deshacer.", style=ft.TextStyle(font_family="AlbertSansB")),
                    ]
                )

            case DeleteFormStyle.PASS_REQ:
                self.title.controls[0].value = "Eliminar registro"

                # Content
                self.content.content = ft.Text(
                    value="¿Desea eliminar este registro? Esta acción ",
                    font_family="AlbertSansL",
                    size=16,
                    spans=[
                        ft.TextSpan(text="no se puede deshacer.", style=ft.TextStyle(font_family="AlbertSansB")),
                    ]
                )

            case DeleteFormStyle.SITE:
                self.title.controls[0].value = "Eliminar sitio web"

                # Content
                self.content.content = ft.Text(
                    value="¿Desea eliminar esta dirección web? Esta acción ",
                    font_family="AlbertSansL",
                    size=16,
                    spans=[
                        ft.TextSpan(text="no se puede deshacer.", style=ft.TextStyle(font_family="AlbertSansB")),
                    ]
                )

            case DeleteFormStyle.USER:
                self.submit_button.on_click = self.__delete
                self.title.controls[0].value = "Eliminar usuario"

                # Content
                self.content.content = ft.Text(
                    value="¿Desea eliminar su cuenta? Esta acción ",
                    font_family="AlbertSansL",
                    size=16,
                    spans=[
                        ft.TextSpan(
                            text="eliminará todos los elementos que estén asociados a ella.",
                            style=ft.TextStyle(font_family="AlbertSansB")
                        ),
                    ]
                )

    def __delete(self, _: ft.ControlEvent) -> None:
        item = session.query(self.item.__class__).filter_by(id=self.item.id).first()
        session.delete(item)
        session.commit()

        if isinstance(self.item, User) and self.item.id == self.user.id:
            self.page.close(self)
            time.sleep(0.4)
            self.__logout_admin()
            return

        self.__update_content()
        self.page.close(self)

    def __update_content(self) -> None:
        self.update_changes()
        if not isinstance(self.update_dropdown, NoneType):
            self.update_dropdown()

    def __logout_admin(self) -> None:
        self.page.session.clear()
        self.__hide_menus()
        self.__nav_to_home()

    def __hide_menus(self) -> None:
        self.page.appbar.visible = False
        self.page.bottom_appbar.visible = False
        self.page.bgcolor = primaryCorporate100
        self.page.clean()
        self.page.update()

    def __nav_to_home(self) -> None:
        # Display loading page
        self.page.overlay.append(LoadingPage())
        self.page.update()

        # Load sound
        close_session = ft.Audio(src="interface/assets/effects/close-session.mp3", autoplay=True)
        self.page.overlay.append(close_session)
        self.page.update()

        # Load login page
        time.sleep(2.5)
        self.page.overlay.clear()
        self.page.go("/login")
