import flet as ft
import time

from data.db_orm import session

from features.models import Note

from interface.pages.forms import DeleteFormStyle, DeleteForm

from shared.utils.masker import mask_text
from shared.utils.colors import *


class NoteWidget(ft.Card):
    def __init__(self, note: Note, page: ft.Page, ) -> None:
        super().__init__()

        # General attributes
        self.page = page
        self.note = note

        # Widget settings
        self.width = 365
        self.height = 310
        self.elevation = 2

        # NoteWidget elements
        self.title = ft.Text(
            self.note.title if self.note.title else "Sin título",
            font_family="AlbertSansB",
            size=18,
            color=titleNoteWidgetColor
        )
        self.note_content = ft.Text(
            mask_text(self.note.encrypted_content)  # TODO: Decrypt content HERE!
        )

        # Widget design
        self.color = bgNoteWidgetColor
        self.shape = ft.RoundedRectangleBorder(4)

        # Widget content
        self.content=ft.Container(
            padding=ft.padding.all(24),
            expand=True,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                spacing=16,
                controls=[
                    ft.Column(
                        controls=[
                            # Title
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    self.title,
                                    ft.Container(
                                        content=ft.Row(
                                            spacing=8,
                                            controls=[
                                                ft.Container(
                                                    on_hover=self.toggle_icon_color,
                                                    content=ft.Icon(
                                                        ft.Icons.EDIT_OUTLINED,
                                                        color=iconAccentSiteWidgetColor
                                                    )
                                                ),
                                                ft.Container(
                                                    on_hover=self.toggle_icon_color,
                                                    on_click=self.open_delete_form,
                                                    content=ft.Icon(
                                                        ft.Icons.DELETE_OUTLINE_ROUNDED,
                                                        color=iconAccentSiteWidgetColor
                                                    )
                                                )
                                            ]
                                        )
                                    )
                                ]
                            ),

                            # Body
                            ft.Row(
                                wrap=True,
                                controls=[
                                    self.note_content
                                ]
                            ),
                        ]
                    ),

                    # Footer
                    ft.Container(
                        on_hover=self.focus_link,
                        on_click=self.show_content,
                        tooltip="Muestra el contenido durante 3 segundos",
                        content=ft.Text(
                            "ver contenido",
                            color=accentTextColor
                        )
                    )
                ]
            )
        )

    @staticmethod
    def focus_link(cursor: ft.ControlEvent) -> None:
        if cursor and cursor.control.content.color == accentTextColor:
            cursor.control.content.color = textNoteWidgetColor
        else:
            cursor.control.content.color = accentTextColor
        cursor.control.update()

    @staticmethod
    def toggle_icon_color(cursor: ft.ControlEvent) -> None:
        if cursor and cursor.control.content.color == iconAccentNoteWidgetColor:
            cursor.control.content.color = iconNoteWidgetColor
        else:
            cursor.control.content.color = iconAccentNoteWidgetColor
        cursor.control.update()

    def show_content(self, cursor: ft.ControlEvent) -> None:
        if cursor:
            self.note_content.value = self.note.encrypted_content  # TODO: Decrypt content HERE!
            self.note_content.update()
            time.sleep(3)
            self.note_content.value = mask_text(self.note.encrypted_content)  # TODO: Decrypt content HERE!
        self.note_content.update()

    def open_delete_form(self, _: ft.ControlEvent) -> None:
        self.page.open(DeleteForm(self.page, self.delete_note, DeleteFormStyle.NOTE))

    def delete_note(self, _: ft.ControlEvent) -> None:
        # New query
        session.query(Note).filter(Note.id == self.note.id).delete()
        session.commit()

