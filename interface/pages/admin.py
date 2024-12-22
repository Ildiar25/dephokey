import flet as ft

from interface.controls import *

from shared.utils.colors import *


class Admin(ft.Container):
    def __init__(self, page: ft.Page) -> None:
        super().__init__()

        # General attributes
        self.page = page
        self.snackbar = ft.SnackBar(
            open=True,
            bgcolor=bgSnackBarDanger,
            content=ft.Text(
                "Testing a new snackbar",
                text_align=ft.TextAlign.CENTER,
                color=mainDangerTextColor
            )
        )

        # Main container settings
        self.expand = True
        self.gradient = ft.LinearGradient(
            bgGradientAdminColor,
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center
        )

        # Admin elements
        self.content = ft.Row(
            controls=[
                ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.AUTO,
                    controls=[
                        ft.Text(
                            "Añadir Usuario:"
                        ),
                        ft.Row(
                            expand=True,
                            controls=[
                                CustomTextField(
                                    label="Nombre Completo",
                                    autofocus=True
                                ),
                                CustomTextField(
                                    label="Usuario"
                                ),
                                CustomTextField(
                                    label="Contraseña",
                                    password=True,
                                    can_reveal_password=True
                                ),
                                CustomElevatedButton(
                                    "AÑADIR",
                                    width=200,
                                    on_click=self.add_new_user
                                )
                            ]
                        ),
                        ft.Row(
                            controls=[
                                ft.Text("Usuarios Añadidos:"),
                                ft.IconButton(ft.Icons.REFRESH, icon_color=colorAdminAccent, on_click=self.update_users)
                            ]
                        ),
                        ft.Row(

                        ),
                        self.snackbar
                    ]
                )
            ]
        )

    def add_new_user(self, _: ft.ControlEvent) -> None:
        fullname: str = self.content.controls[0].controls[1].controls[0].value
        username: str = self.content.controls[0].controls[1].controls[1].value
        password: str = self.content.controls[0].controls[1].controls[2].value

    def update_users(self, _: ft.ControlEvent) -> None:
        print("users = session.query(User).all()")
        self.content.controls[0].controls[3].controls.append(ft.Container())
