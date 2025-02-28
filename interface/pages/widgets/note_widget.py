import flet as ft
from typing import Callable

from data.db_orm import session

from features.models import Note
from features.data_encryption.core import decrypt_data

from interface.controls import IconLink, IconLinkStyle
from interface.pages.forms.base_form import FormStyle
from interface.pages.forms import DeleteFormStyle, DeleteForm, NoteForm

from shared.utils.masker import mask_text
from shared.utils.colors import *


class NoteWidget(ft.Card):
    def __init__(self, note: Note, page: ft.Page, update_appearance: Callable[[], None]) -> None:
        super().__init__()

        # General attributes
        self.page = page
        self.note = note
        self.update_appearance = update_appearance

        # Widget settings
        self.width = 365
        self.height = 310
        self.elevation = 2
        self.animate_scale = ft.animation.Animation(200, ft.AnimationCurve.EASE_IN_OUT)

        # NoteWidget elements
        self.note_title = ft.Text(self.note.title if self.note.title else "Sin título", font_family="AlbertSansB",
            size=18, color=titleNoteWidgetColor)
        self.note_content = ft.Text(mask_text(decrypt_data(self.note.encrypted_content)))

        # Widget design
        self.color = bgNoteWidgetColor
        self.shape = ft.RoundedRectangleBorder(4)

        # Widget content
        self.content=ft.Container(
            on_hover=self.scale_widget,
            padding=ft.padding.all(24),
            expand=True,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                spacing=16,
                controls=[
                    ft.Column(
                        controls=[
                            # Header
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    self.note_title,
                                    ft.Container(
                                        content=ft.Row(
                                            spacing=8,
                                            controls=[
                                                IconLink(ft.Icons.EDIT_OUTLINED, IconLinkStyle.LIGHT,
                                                         function=self.open_edit_note_form),
                                                IconLink(ft.Icons.DELETE_OUTLINED, IconLinkStyle.LIGHT,
                                                         function=self.open_delete_form)
                                            ]
                                        )
                                    )
                                ]
                            ),

                            # Body
                            ft.Row(
                                wrap=True,
                                controls=[
                                    ft.Container(
                                        on_hover=self.show_content,
                                        content=ft.Row(
                                            wrap=True,
                                            controls=[
                                                self.note_content
                                            ]
                                        )
                                    )
                                ]
                            )
                        ]
                    )
                ]
            )
        )

    def scale_widget(self, cursor: ft.ControlEvent) -> None:
        if cursor and self.scale == 1.05:
            self.scale = 1
        else:
            self.scale = 1.05
        self.update()

    def show_content(self, cursor: ft.ControlEvent) -> None:
        if cursor and self.note_content.value == mask_text(decrypt_data(self.note.encrypted_content)):
            self.note_content.value = decrypt_data(self.note.encrypted_content)
        else:
            self.note_content.value = mask_text(decrypt_data(self.note.encrypted_content))
        self.note_content.update()

    def open_edit_note_form(self, _: ft.ControlEvent) -> None:
        self.page.open(
            NoteForm(title=f"Editando {self.note.title}", page=self.page, style=FormStyle.EDIT,
                     note=self.note, update_changes=self.update_appearance)
        )

    def open_delete_form(self, _: ft.ControlEvent) -> None:
        self.page.open(DeleteForm(self.page, self.delete_note, DeleteFormStyle.NOTE))

    def delete_note(self, _: ft.ControlEvent) -> None:
        # New query
        session.query(Note).filter(Note.id == self.note.id).delete()
        session.commit()
        self.update_appearance()
