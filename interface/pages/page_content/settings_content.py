import flet as ft

from data.db_orm import session

from features.models.user import User

from interface.controls import CustomElevatedButton, ButtonStyle, CustomTextField, Snackbar, SnackbarStyle
from interface.pages.forms.base_form import FormStyle
from interface.pages.forms import ChangePasswordForm

from shared.validate import Validate
from shared.utils.colors import *


class SettingsPage(ft.Row):
    def __init__(self, page: ft.Page, snackbar: Snackbar) -> None:
        super().__init__()

        # General attributes
        self.page = page
        self.snackbar = snackbar

        # Settings attributes
        self.user: User = self.page.session.get("session")
        self.fullname = CustomTextField(
            value=self.user.fullname, expand=True, on_change=self.toggle_empty_fields, max_length=30)
        self.email = CustomTextField(
            value=self.user.email, expand=True, on_change=self.toggle_empty_fields, max_length=30)
        self.password = CustomTextField(
            value="*" * 17, expand=True, password=True, read_only=True)

        # Design settings
        self.spacing = 32

        # Settings content
        self.controls = [
            ft.Container(
                height=334,
                expand=True,
                bgcolor=bgGeneralFormColor,
                border_radius=4,
                padding=ft.padding.all(24),
                shadow=ft.BoxShadow(
                    blur_radius=0.9, offset=(0.0, 0.5), color=ft.Colors.with_opacity(opacity=0.3, color=neutral80)
                ),
                content=ft.Column(
                    spacing=24,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Text(
                                    value="Información general", size=24, color=accentTextColor
                                )
                            ]
                        ),
                        ft.Row(
                            controls=[
                                ft.Column(
                                    expand=True,
                                    spacing=8,
                                    controls=[
                                        ft.Text(
                                            value="Nombre completo:", font_family="AlbertSansL",
                                            size=16, color=primaryTextColor
                                        ),
                                        ft.Row(controls=[self.fullname]),
                                        ft.Text(
                                            value="Correo electrónico:", font_family="AlbertSansL",
                                            size=16, color=primaryTextColor
                                        ),
                                        ft.Row(controls=[self.email])
                                    ]
                                )
                            ]
                        ),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.END,
                            controls=[
                                CustomElevatedButton(
                                    name="Guardar", style=ButtonStyle.DEFAULT, on_click=self.save_changes
                                )
                            ]
                        )
                    ]
                )
            ),
            ft.Container(
                height=334,
                expand=True,
                bgcolor=bgGeneralFormColor,
                border_radius=4,
                padding=ft.padding.all(24),
                shadow=ft.BoxShadow(
                    blur_radius=0.9, offset=(0.0, 0.5), color=ft.Colors.with_opacity(opacity=0.3, color=neutral80)
                ),
                content=ft.Column(
                    spacing=24,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Text(
                                    value="Seguridad", size=24, color=accentTextColor
                                )
                            ]
                        ),
                        ft.Row(
                            controls=[
                                ft.Column(
                                    expand=True,
                                    spacing=8,
                                    controls=[
                                        ft.Text(
                                            value="Contraseña:", font_family="AlbertSansL",
                                            size=16, color=primaryTextColor
                                        ),
                                        ft.Row(controls=[self.password]),
                                        ft.Text(
                                            value="", font_family="AlbertSansL",
                                            size=16, color=primaryTextColor
                                        ),
                                        ft.Row(controls=[CustomTextField(disabled=True, border_width=0)])
                                    ]
                                )
                            ]
                        ),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.END,
                            controls=[
                                CustomElevatedButton(
                                    name="Cambiar contraseña", style=ButtonStyle.CANCEL, on_click=self.change_password
                                )
                            ]
                        )
                    ]
                )
            )
        ]

        self.update_content()

    def update_content(self) -> None:
        self.fullname.value = self.user.fullname
        self.email.value = self.user.email

    def save_changes(self, _: ft.ControlEvent) -> None:
        new_fullname: str = self.fullname.value.title().strip()
        new_email: str = self.email.value.lower().strip()

        if self.user.fullname == new_fullname and self.user.email == new_email:
            self.snackbar.change_style(
                msg="¡No se ha realizado ningún cambio!\nLos datos guardados son iguales.", style=SnackbarStyle.INFO
            )
            self.snackbar.update()
            return

        # Update user data
        if all([new_fullname, new_email]):
            if not Validate.is_valid_email(new_email):
                self.email.error_text = "El correo no es válido."
                self.email.update()
                return

            self.user.fullname = new_fullname
            self.user.email = new_email
            session.commit()

            # Updates settings content
            self.fullname.value = self.user.fullname
            self.email.value = self.user.email
            self.update()

            # Notifes the user
            self.snackbar.change_style(msg="¡Datos actualizados!", style=SnackbarStyle.SUCCESS)
            self.snackbar.update()

    def change_password(self, _: ft.ControlEvent) -> None:
        self.page.open(
            ChangePasswordForm(page=self.page, snackbar=self.snackbar, style=FormStyle.EDIT)
        )

    @staticmethod
    def toggle_empty_fields(field: ft.ControlEvent) -> None:
        if field and not field.control.value:
            field.control.error_text = "El campo no puede estar vacío."
        else:
            field.control.error_text = None
        field.control.update()
