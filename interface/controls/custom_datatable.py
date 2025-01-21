import flet as ft
from typing import List, Type

from features.models.user import User
from features.models import *


class CustomDatatable(ft.DataTable):
    def __init__(self, columns: List[ft.DataColumn]) -> None:
        super().__init__(columns=columns)

        self.expand = True
        self.border_radius = 8
        self.border = ft.border.all(1, ft.Colors.PURPLE_900)
        self.bgcolor = ft.Colors.WHITE
        self.data_row_color = {
            ft.ControlState.HOVERED: ft.Colors.GREY_100
        }

    def load_items(self, items: dict, model: Type[User | CreditCard | Note | Site]) -> None:
        if not items:
            pass
        else:
            if model is User:
                for value in items.values():
                    new_row = ft.DataRow(
                        on_select_changed=lambda e: print(e.control.cells[0].content.value),
                        cells=[
                            ft.DataCell(ft.Text(value.get("id", "-"))),
                            ft.DataCell(ft.Text(value.get("role", "-"))),
                            ft.DataCell(ft.Text(value.get("fullname", "-"))),
                            ft.DataCell(ft.Text(value.get("email", "-"))),
                            ft.DataCell(ft.Text(value.get("hashed_password", "-"))),
                            ft.DataCell(ft.Text(value.get("created", "-"))),
                        ]
                    )
                    self.rows.append(new_row)

            if model is CreditCard:
                pass

            if model is Note:
                pass

            if model is Site:
                pass
