import flet as ft
from typing import Callable

from data.db_orm import session

from features.data_encryption.core import decrypt_data, encrypt_data
from features.models.user import User
from features.models import Note

from .base_form import BaseForm, FormStyle
from interface.controls import CustomTextField, Snackbar, SnackbarStyle

from shared.utils.colors import *


class NoteForm(BaseForm):
    def __init__(self,
                 title: str, page: ft.Page, style: FormStyle, snackbar: Snackbar | None = None,
                 note: Note | None = None, update_changes: Callable[[], None] = None) -> None:
        super().__init__()

        # General attributes
        self.page = page
        self.snackbar = snackbar
        self.style = style
        self.note = note
        self.update_changes = update_changes

        # Form attributes
        self.user: User = self.page.session.get("session")

        # Form fields
        self.n_title = CustomTextField(hint_text="Añade un título", max_length=24,
            on_change=self.__update_field_inputs
        )
        self.n_content = CustomTextField(hint_text="Agrega contenido importante", can_reveal_password=True,
            password=True, on_change=self.__update_field_inputs, max_lines=10, min_lines=10, max_length=324,
        )

        # Form settings
        self.cancel_button.on_click = lambda _: self.page.close(self)

        # Form title
        self.title = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text(title, font_family="AlbertSansB", size=20, color=primaryTextColor), self.close_button
            ]
        )

        self.__update_appearance()

    def __update_appearance(self) -> None:
        match self.style:
            case FormStyle.ADD:
                self.submit_button.on_click = self.__add_note

                # Content
                self.content.content = ft.Column(
                    spacing=14,
                    controls=[
                        ft.Column(spacing=6, controls=[
                            ft.Text(value="Título de la nota", font_family="AlbertSansR", color=primaryTextColor),
                            self.n_title
                        ]),
                        ft.Column(spacing=6, controls=[
                            ft.Text(value="Contenido", font_family="AlbertSansR", color=primaryTextColor,
                                    spans=[self.span]),
                            self.n_content
                        ])
                    ]
                )

            case FormStyle.EDIT:
                self.submit_button.on_click = self.__update_note
                self.n_title.value = self.note.title
                self.n_content.value = decrypt_data(self.note.encrypted_content)

                # Content
                self.content.content = ft.Column(
                    spacing=14,
                    controls=[
                        ft.Column(spacing=6, controls=[
                            ft.Text(value="Título de la nota", font_family="AlbertSansR", color=primaryTextColor),
                            self.n_title
                        ]),
                        ft.Column(spacing=6, controls=[
                            ft.Text(value="Contenido", font_family="AlbertSansR", color=primaryTextColor,
                                    spans=[self.span]),
                            self.n_content
                        ])
                    ]
                )

    def __update_field_inputs(self, cursor: ft.ControlEvent) -> None:
        self.n_content.reset_error()
        self.fields = [self.n_content.value]
        self.toggle_submit_button_state(cursor)

    def __update_note(self, _: ft.ControlEvent) -> None:

        new_title = self.n_title.value.capitalize().strip() if self.n_title.value else "Nueva nota"
        new_content = self.n_content.value.strip()

        if not new_content:
            self.n_content.show_error("El campo no puede ir vacío.")
            return

        # Update note-data
        self.note.title = new_title
        self.note.encrypted_content = encrypt_data(new_content)

        session.commit()
        self.update_changes()
        self.page.close(self)

    def __add_note(self, _: ft.ControlEvent) -> None:

        new_title = self.n_title.value.capitalize().strip() if self.n_title.value else "Nueva nota"
        new_content = self.n_content.value.strip()

        if not new_content:
            self.n_content.show_error("El campo no puede ir vacío.")
            return

        # Create new note-instance
        new_note = Note(new_content, self.user, new_title)
        session.add(new_note)
        session.commit()

        self.update_changes()
        self.snackbar.change_style(msg=f"¡{new_title} añadida!", style=SnackbarStyle.SUCCESS)
        self.snackbar.update()
        self.page.close(self)
