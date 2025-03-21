import flet as ft

from data.db_orm import session
from features.models.user import User
from interface.controls import CustomElevatedButton, CustomTextField
from interface.controls.e_button import ButtonStyle
from interface.controls.snackbar import Snackbar, SnackbarStyle
from interface.pages.forms import ChangePasswordForm, DeleteForm
from interface.pages.forms.base_form import FormStyle
from interface.pages.forms.delete_form import DeleteFormStyle
from shared.utils.colors import accentTextColor, neutral00, neutral80, primaryTextColor, transparentColor
from shared.validate import Validate


class SettingsPage(ft.Row):
    """Displays two forms. One for show user data and the other one for account settings."""
    def __init__(self, page: ft.Page, snackbar: Snackbar) -> None:
        super().__init__()

        # General attributes
        self.page = page
        self.snackbar = snackbar

        # Settings attributes
        self.user: User = self.page.session.get("session")
        self.fullname = CustomTextField(
            value=self.user.fullname,
            expand=True,
            on_change=self.__toggle_empty_fields,
            max_length=30
        )
        self.email = CustomTextField(
            value=self.user.email,
            expand=True,
            on_change=self.__toggle_empty_fields,
            on_submit=self.__save_changes,
            max_length=30
        )
        self.password = CustomTextField(
            value="*" * 17,
            expand=True,
            password=True,
            read_only=True
        )

        # Settings design
        self.spacing = 32

        # Settings content
        self.controls = [
            ft.Container(
                height=334,
                expand=True,
                bgcolor=neutral00,
                border_radius=4,
                padding=ft.padding.all(24),
                shadow=ft.BoxShadow(
                    blur_radius=0.9,
                    offset=(0.0, 0.5),
                    color=ft.Colors.with_opacity(opacity=0.3, color=neutral80)
                ),
                content=ft.Column(
                    spacing=24,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Text(
                                    value="Información general", size=24, color=accentTextColor
                                ),
                            ]
                        ),
                        ft.Divider(color=transparentColor),
                        ft.Row(
                            controls=[
                                ft.Column(
                                    expand=True,
                                    spacing=8,
                                    controls=[
                                        ft.Text(
                                            value="Nombre completo:",
                                            font_family="AlbertSansL",
                                            size=16,
                                            color=primaryTextColor
                                        ),
                                        ft.Row(
                                            controls=[self.fullname, ]
                                        ),
                                        ft.Text(
                                            value="Correo electrónico:",
                                            font_family="AlbertSansL",
                                            size=16,
                                            color=primaryTextColor
                                        ),
                                        ft.Row(
                                            controls=[self.email, ]
                                        ),
                                    ]
                                ),
                            ]
                        ),
                        ft.Column(expand=True),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.END,
                            controls=[
                                CustomElevatedButton(
                                    name="Guardar", style=ButtonStyle.DEFAULT, on_click=self.__save_changes
                                ),
                            ]
                        ),
                    ]
                )
            ),
            ft.Container(
                height=334,
                expand=True,
                bgcolor=neutral00,
                border_radius=4,
                padding=ft.padding.all(24),
                shadow=ft.BoxShadow(
                    blur_radius=0.9,
                    offset=(0.0, 0.5),
                    color=ft.Colors.with_opacity(opacity=0.3, color=neutral80)
                ),
                content=ft.Column(
                    spacing=24,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Text(
                                    value="Seguridad", size=24, color=accentTextColor
                                ),
                            ]
                        ),
                        ft.Divider(color=transparentColor),
                        ft.Row(
                            controls=[
                                ft.Column(
                                    alignment=ft.MainAxisAlignment.START,
                                    expand=True,
                                    spacing=8,
                                    controls=[
                                        ft.Text(
                                            value="Contraseña:",
                                            font_family="AlbertSansL",
                                            size=16,
                                            color=primaryTextColor
                                        ),
                                        ft.Row(
                                            controls=[self.password, ]
                                        ),
                                    ]
                                ),
                            ]
                        ),
                        ft.Column(expand=True),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                CustomElevatedButton(
                                    name="Eliminar cuenta",
                                    style=ButtonStyle.DEFAULT,
                                    on_click=self.__open_delete_form
                                ),
                                CustomElevatedButton(
                                    name="Cambiar contraseña",
                                    style=ButtonStyle.CANCEL,
                                    on_click=self.__change_password
                                ),
                            ]
                        ),
                    ]
                )
            ),
        ]

        self.update_content()

    def update_content(self) -> None:
        self.fullname.value = self.user.fullname
        self.email.value = self.user.email

    def __save_changes(self, _: ft.ControlEvent) -> None:
        new_fullname: str = self.fullname.value.title().strip()
        new_email: str = self.email.value.lower().strip()

        if self.user.fullname == new_fullname and self.user.email == new_email:
            self.__display_message(
                msg="¡No se ha realizado ningún cambio!\nLos datos guardados son iguales.", style=SnackbarStyle.INFO
            )
            return

        # Update user data
        if all([new_fullname, new_email]) and not Validate.is_valid_email(new_email):
            self.email.error_text = "El correo no es válido."
            self.email.update()
            return

        self.user.fullname = new_fullname
        self.user.email = new_email
        session.commit()

        self.__update_settings_content()

        # Provide user feedback
        self.__display_message(msg="¡Datos actualizados!", style=SnackbarStyle.SUCCESS)

    def __update_settings_content(self) -> None:
        self.fullname.value = self.user.fullname
        self.email.value = self.user.email
        self.update()

    def __open_delete_form(self, _: ft.ControlEvent) -> None:
        self.page.open(
            DeleteForm(page=self.page, item=self.user, style=DeleteFormStyle.USER, snackbar=self.snackbar)
        )

    def __change_password(self, _: ft.ControlEvent) -> None:
        self.page.open(
            ChangePasswordForm(page=self.page, snackbar=self.snackbar, style=FormStyle.PW_UPDATE)
        )

    def __display_message(self, msg: str, style: SnackbarStyle) -> None:
        self.snackbar.change_style(msg=msg, style=style)
        self.snackbar.update()

    @staticmethod
    def __toggle_empty_fields(field: ft.ControlEvent) -> None:
        if field and not field.control.value:
            field.control.error_text = "El campo no puede estar vacío."
        else:
            field.control.error_text = None

        field.control.update()
