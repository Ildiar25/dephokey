import flet as ft

from features.models.user import User


class UserWidget(ft.Card):
    def __init__(self, user: User) -> None:
        super().__init__()

        # General attributes
        self.user = user
        self.delete_button = ft.IconButton(
            ft.Icons.DELETE
        )

        self.cells = [
            ft.DataCell(
                ft.Text(user.id)
            )
        ]
