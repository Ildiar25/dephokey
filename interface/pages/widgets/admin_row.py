import flet as ft
from enum import Enum
from typing import Union, Callable

from features.models.user import User
from features.models import *
from features.data_encryption.core import decrypt_data

from interface.controls import IconLink, IconLinkStyle
from interface.pages.forms.base_form import FormStyle
from interface.pages.forms import DeleteForm, DeleteFormStyle, SiteForm, CreditCardForm, NoteForm, UserForm, ResetPasswordForm


class RowStyle(Enum):
    USER = "user"
    SITE = "site"
    CREDITCARD = "creditcard"
    NOTE = "note"
    PASS_REQUEST = "pass_request"


class AdminRow(ft.Container):
    def __init__(self, page: ft.Page,
                 item: Union[User, Site, CreditCard, Note, PasswordRequest], style: RowStyle,
                 update_appearance: Callable[[], None], update_dropdown: Callable[[], None]) -> None:
        super().__init__()

        # General attributes
        self.page = page
        self.item = item
        self.style = style
        self.update_appearance = update_appearance
        self.update_dropdown = update_dropdown

        # Row attributes
        self.actions = ft.Row(
            spacing=5,
            controls=[
                IconLink(ft.Icons.EDIT_OUTLINED, IconLinkStyle.LIGHT, function=self.open_edit_item_form, visible=False),
                IconLink(ft.Icons.DELETE_OUTLINED, IconLinkStyle.LIGHT, function=self.open_delete_form, visible=False)
            ]
        )

        # Row design
        self.expand = True
        self.padding = ft.padding.all(10)
        self.on_hover = self.toggle_visible_buttons

        # Content
        self.content = ft.Row(
            height=20,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[]
        )
        self.__change_appearance()

    def __change_appearance(self) -> None:
        match self.style:
            case RowStyle.USER:
                self.content.controls.extend([
                    ft.Column(width=148, controls=[ft.Text(self.item.id)]),
                    ft.Column(width=78, controls=[ft.Text(self.item.role.value.upper())]),
                    ft.Column(width=156, controls=[ft.Text(self.item.fullname)]),
                    ft.Column(width=186, controls=[ft.Text(self.item.email)]),
                    ft.Column(width=148, controls=[ft.Text(self.item.created.strftime("%d/%m/%Y | %H:%M:%S"))]),
                    ft.Column(width=56, controls=[self.actions])
                ])

            case RowStyle.SITE:
                self.content.controls.extend([
                    ft.Column(width=148, controls=[ft.Text(self.item.id)]),
                    ft.Column(width=186, controls=[ft.Text(self.item.user.email)]),
                    ft.Column(width=156, controls=[ft.Text(self.item.name)]),
                    ft.Column(width=186, controls=[ft.Text(self.item.address)]),
                    ft.Column(width=186, controls=[ft.Text(self.item.username)]),
                    ft.Column(width=148, controls=[ft.Text(self.item.created.strftime("%d/%m/%Y | %H:%M:%S"))]),
                    ft.Column(width=56, controls=[self.actions])
                ])

            case RowStyle.CREDITCARD:
                self.content.controls.extend([
                    ft.Column(width=148, controls=[ft.Text(self.item.id)]),
                    ft.Column(width=186, controls=[ft.Text(self.item.user.email)]),
                    ft.Column(width=152, controls=[ft.Text(decrypt_data(self.item.encrypted_number))]),
                    ft.Column(width=186, controls=[ft.Text(self.item.alias)]),
                    ft.Column(width=186, controls=[ft.Text(self.item.cardholder)]),
                    ft.Column(width=148, controls=[ft.Text(self.item.created.strftime("%d/%m/%Y | %H:%M:%S"))]),
                    ft.Column(width=56, controls=[self.actions])
                ])

            case RowStyle.NOTE:
                self.content.controls.extend([
                    ft.Column(width=148, controls=[ft.Text(self.item.id)]),
                    ft.Column(width=186, controls=[ft.Text(self.item.user.email)]),
                    ft.Column(width=152, controls=[ft.Text(self.item.title)]),
                    ft.Column(width=148, controls=[ft.Text(self.item.created.strftime("%d/%m/%Y | %H:%M:%S"))]),
                    ft.Column(width=56, controls=[self.actions])
                ])

            case RowStyle.PASS_REQUEST:
                self.content.controls.extend([
                    ft.Column(width=148, controls=[ft.Text(self.item.id)]),
                    ft.Column(width=186, controls=[ft.Text(self.item.user.email)]),
                    ft.Column(width=152, controls=[ft.Text(decrypt_data(self.item.encrypted_code))]),
                    ft.Column(width=148, controls=[ft.Text(self.item.created.strftime("%d/%m/%Y | %H:%M:%S"))]),
                    ft.Column(width=56, controls=[self.actions])
                ])

    def toggle_visible_buttons(self, cursor: ft.ControlEvent) -> None:
        if cursor and all((self.actions.controls[0].visible == False, self.actions.controls[1].visible == False)):
            self.actions.controls[0].visible = True
            self.actions.controls[1].visible = True
        else:
            self.actions.controls[0].visible = False
            self.actions.controls[1].visible = False
        self.actions.controls[0].update()
        self.actions.controls[1].update()

    def open_edit_item_form(self, _: ft.ControlEvent) -> None:
        match self.style:
            case RowStyle.USER:
                self.page.open(
                    UserForm(title=f"Editando {self.item.fullname}", user=self.item, page=self.page,
                             style=FormStyle.EDIT, update_changes=self.update_appearance,
                             update_dropdown=self.update_dropdown)
                )
            case RowStyle.SITE:
                self.page.open(
                    SiteForm(title=f"Editando {self.item.name}", site= self.item, page=self.page, style=FormStyle.EDIT,
                             update_changes=self.update_appearance, update_dropdown=self.update_dropdown)
                )
            case RowStyle.CREDITCARD:
                self.page.open(
                    CreditCardForm(title=f"Editando {self.item.alias}", page=self.page, style=FormStyle.EDIT,
                                   update_changes=self.update_appearance, update_dropdown=self.update_dropdown,
                                   creditcard=self.item)
                )
            case RowStyle.NOTE:
                self.page.open(
                    NoteForm(title=f"Editando {self.item.title}", page=self.page, style=FormStyle.EDIT, note=self.item,
                             update_changes=self.update_appearance, update_dropdown=self.update_dropdown)
                )
            case RowStyle.PASS_REQUEST:
                self.page.open(
                    ResetPasswordForm(title="Editando Token", page=self.page, style=FormStyle.EDIT,
                                      password_request=self.item, update_changes=self.update_appearance,
                                      update_dropdown=self.update_dropdown)
                )

    def open_delete_form(self, _: ft.ControlEvent) -> None:
        match self.style:
            case RowStyle.USER:
                self.page.open(
                    DeleteForm(
                        self.page, self.item, DeleteFormStyle.USER,
                        self.update_appearance, update_dropdown=self.update_dropdown
                    )
                )

            case RowStyle.SITE:
                self.page.open(
                    DeleteForm(
                        self.page, self.item, DeleteFormStyle.SITE,
                        self.update_appearance, update_dropdown=self.update_dropdown
                    )
                )

            case RowStyle.CREDITCARD:
                self.page.open(
                    DeleteForm(
                        self.page, self.item, DeleteFormStyle.CREDITCARD,
                        self.update_appearance, update_dropdown=self.update_dropdown
                    )
                )

            case RowStyle.NOTE:
                self.page.open(
                    DeleteForm(
                        self.page, self.item, DeleteFormStyle.NOTE,
                        self.update_appearance, update_dropdown=self.update_dropdown
                    )
                )

            case RowStyle.PASS_REQUEST:
                self.page.open(
                    DeleteForm(
                        self.page, self.item, DeleteFormStyle.PASS_REQ,
                        self.update_appearance, update_dropdown=self.update_dropdown
                    )
                )
