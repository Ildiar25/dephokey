import datetime

import flet as ft
import datetime as dt

from data.db_orm import session

from features.models.user import User

from interface.controls import CustomTextField, CustomElevatedButton, CustomSwitch, DatePicker

from shared.utils.colors import *


class Admin(ft.Column):
    def __init__(self, page: ft.Page) -> None:
        super().__init__()

        # General attributes
        self.page = page
        self.admin = self.page.session.get("session")
        self.users = session.query(User).all()
        self.creation_date = dt.datetime.today()

        self.user_datepicker = DatePicker(self.page, self.update_date_userform)
        self.site_datepicker = DatePicker(self.page, self.update_date_siteform)
        self.creditcard_datepicker = DatePicker(self.page, self.update_date_creditcardform)
        self.note_datepicker = DatePicker(self.page, self.update_date_noteform)


        #Admin attributes
        self.submit_user = CustomElevatedButton(
            name="Añadir Usuario", expand=True, icon=ft.Icons.ADD_ROUNDED, foreground_color=tertiaryTextColor,
            bg_color=primaryCorporateColor, border_size=-1, on_click=self.test01)
        self.submit_site = CustomElevatedButton(
            name="Añadir Dirección", expand=True, icon=ft.Icons.ADD_ROUNDED, foreground_color=tertiaryTextColor,
            bg_color=primaryCorporateColor, border_size=-1, on_click=self.test01)
        self.submit_creditcard = CustomElevatedButton(
            name="Añadir Tarjeta", expand=True, icon=ft.Icons.ADD_ROUNDED, foreground_color=tertiaryTextColor,
            bg_color=primaryCorporateColor, border_size=-1, on_click=self.test01)
        self.submit_note = CustomElevatedButton(
            name="Añadir Nota", expand=True, icon=ft.Icons.ADD_ROUNDED, foreground_color=tertiaryTextColor,
            bg_color=primaryCorporateColor, border_size=-1, on_click=self.test01)
        self.dropdown = ft.Dropdown(
            label="Selecciona un correo",
            label_style=ft.TextStyle(color=secondaryTextColor),
            select_icon=ft.Icons.KEYBOARD_ARROW_DOWN_ROUNDED,
            icon_enabled_color=primaryCorporateColor,
            bgcolor=bgGeneralFormColor,
            width=310,
            border_color=neutral20,
            focused_border_color=primaryCorporateColor,
            border_radius=4,
            options=[ft.dropdown.Option(user.email) for user in self.users]
        )

        # Forms
        self.newuser_form = [
            ft.Column(
                spacing=22,
                controls=[
                    ft.Row(
                        controls=[
                            CustomTextField(label="Nombre completo", expand=True,),
                            CustomTextField(label="Correo electrónico", expand=True),
                            CustomTextField(label="Contraseña", expand=True, password=True, can_reveal_password=True),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            CustomTextField(label="Fecha de creación", expand=True,
                                            value=dt.datetime.today().strftime("%d/%m/%Y"), read_only=True),
                            ft.IconButton(
                                ft.Icons.CALENDAR_MONTH_ROUNDED,
                                icon_color=primaryCorporateColor,
                                on_click=lambda _: self.page.open(self.user_datepicker),
                                highlight_color=selectedIconGeneralFormColor,
                                hover_color=hoverIconGeneralFormColor,
                                tooltip="Seleccionar fecha"
                            ),
                            CustomTextField(expand=True, disabled=True),
                            CustomSwitch(title="Administrador", width=200),
                        ]
                    ),
                    ft.Row(controls=[self.submit_user])
                ]
            )
        ]
        self.newsite_form = [
            ft.Column(
                spacing=22,
                controls=[
                    ft.Row(
                        controls=[
                            self.dropdown,
                            CustomTextField(label="Nombre (opcional)", expand=True),
                            CustomTextField(label="Dirección", expand=True),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            CustomTextField(label="Usuario", expand=True),
                            CustomTextField(label="Contraseña", expand=True),
                            CustomTextField(label="Fecha de creación", expand=True,
                                            value=dt.datetime.today().strftime("%d/%m/%Y"), read_only=True),
                            ft.IconButton(
                                ft.Icons.CALENDAR_MONTH_ROUNDED,
                                icon_color=primaryCorporateColor,
                                on_click=lambda _: self.page.open(self.site_datepicker),
                                highlight_color=selectedIconGeneralFormColor,
                                hover_color=hoverIconGeneralFormColor,
                                tooltip="Seleccionar fecha"
                            )
                        ]
                    ),
                    ft.Row(controls=[self.submit_site])
                ]
            )
        ]
        self.newcreditcard_form = [
            ft.Column(
                spacing=22,
                controls=[
                    ft.Row(
                        controls=[
                            self.dropdown,
                            CustomTextField(label="Alias (Opcional)", expand=True),
                            CustomTextField(label="Titular", expand=True),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            CustomTextField(label="Número de la tarjeta", expand=True),
                            CustomTextField(label="Fecha de caducidad", expand=True, read_only=True),
                            ft.IconButton(
                                ft.Icons.CALENDAR_MONTH_ROUNDED,
                                icon_color=primaryCorporateColor,
                                highlight_color=selectedIconGeneralFormColor,
                                hover_color=hoverIconGeneralFormColor,
                                tooltip="Seleccionar fecha"
                            ),
                            CustomTextField(label="CVC", width=64),
                            CustomTextField(label="Fecha de creación", expand=True,
                                            value=self.creation_date.strftime("%d/%m/%Y"), read_only=True),
                            ft.IconButton(
                                ft.Icons.CALENDAR_MONTH_ROUNDED,
                                icon_color=primaryCorporateColor,
                                on_click=lambda _: self.page.open(self.creditcard_datepicker),
                                highlight_color=selectedIconGeneralFormColor,
                                hover_color=hoverIconGeneralFormColor,
                                tooltip="Seleccionar fecha"
                            )
                        ]
                    ),
                    ft.Row(controls=[self.submit_creditcard])
                ]
            )
        ]
        self.newnote_form = [
            ft.Column(
                spacing=22,
                controls=[
                    ft.Row(
                        controls=[
                            self.dropdown,
                            CustomTextField(label="Título (Opcional)", expand=True),
                            CustomTextField(label="Fecha de creación", expand=True,
                                            value=self.creation_date.strftime("%d/%m/%Y"), read_only=True),
                            ft.IconButton(
                                ft.Icons.CALENDAR_MONTH_ROUNDED,
                                icon_color=primaryCorporateColor,
                                on_click=lambda _: self.page.open(self.note_datepicker),
                                highlight_color=selectedIconGeneralFormColor,
                                hover_color=hoverIconGeneralFormColor,
                                tooltip="Seleccionar fecha"
                            )
                        ]
                    ),
                    ft.Row(
                        controls=[
                            CustomTextField(label="Contenido", max_lines=2, expand=True)
                        ]
                    ),
                    ft.Row(controls=[self.submit_note])
                ]
            )
        ]


        # Main settings
        self.spacing = 32

        # Expansion Tiles
        self.controls = [
            # Add new user
            ft.Container(
                expand=True,
                shadow=ft.BoxShadow(blur_radius=0.9, offset=(0.0, 0.5),
                                    color=ft.Colors.with_opacity(opacity=0.3, color=neutral80)),
                border_radius=4,
                content=ft.ExpansionTile(
                    title=ft.Text(value="Usuarios", font_family="AlbertSansR", size=20, color=accentTextColor),
                    controls_padding=ft.padding.all(22),
                    shape=ft.RoundedRectangleBorder(4),
                    collapsed_shape=ft.RoundedRectangleBorder(4),
                    min_tile_height=88,
                    bgcolor=neutral00,
                    collapsed_bgcolor=neutral00,
                    controls=self.newuser_form
                )
            ),

            # Add new site
            ft.Container(
                expand=True,
                shadow=ft.BoxShadow(blur_radius=0.9, offset=(0.0, 0.5),
                                    color=ft.Colors.with_opacity(opacity=0.3, color=neutral80)),
                border_radius=4,
                content=ft.ExpansionTile(
                    title=ft.Text(value="Direcciones Web", font_family="AlbertSansR", size=20,
                                  color=accentTextColor),
                    controls_padding=ft.padding.all(22),
                    shape=ft.RoundedRectangleBorder(4),
                    collapsed_shape=ft.RoundedRectangleBorder(4),
                    min_tile_height=88,
                    bgcolor=neutral00,
                    collapsed_bgcolor=neutral00,
                    controls=self.newsite_form
                )
            ),

            # Add new creditcard
            ft.Container(
                expand=True,
                shadow=ft.BoxShadow(blur_radius=0.9, offset=(0.0, 0.5),
                                    color=ft.Colors.with_opacity(opacity=0.3, color=neutral80)),
                border_radius=4,
                content=ft.ExpansionTile(
                    title=ft.Text(value="Tarjetas de Crédito", font_family="AlbertSansR", size=20,
                                  color=accentTextColor),
                    controls_padding=ft.padding.all(22),
                    shape=ft.RoundedRectangleBorder(4),
                    collapsed_shape=ft.RoundedRectangleBorder(4),
                    min_tile_height=88,
                    bgcolor=neutral00,
                    collapsed_bgcolor=neutral00,
                    controls=self.newcreditcard_form
                )
            ),

            # Add new note
            ft.Container(
                expand=True,
                shadow=ft.BoxShadow(blur_radius=0.9, offset=(0.0, 0.5),
                                    color=ft.Colors.with_opacity(opacity=0.3, color=neutral80)),
                border_radius=4,
                content=ft.ExpansionTile(
                    title=ft.Text(value="Notas Seguras", font_family="AlbertSansR", size=20,
                                  color=accentTextColor),
                    controls_padding=ft.padding.all(22),
                    shape=ft.RoundedRectangleBorder(4),
                    collapsed_shape=ft.RoundedRectangleBorder(4),
                    min_tile_height=88,
                    bgcolor=neutral00,
                    collapsed_bgcolor=neutral00,
                    controls=self.newnote_form
                )
            ),
        ]

    def update_date_userform(self, new_date: datetime.datetime) -> None:
        self.newuser_form[0].controls[1].controls[0].value = new_date.strftime("%d/%m/%Y")
        self.newuser_form[0].controls[1].controls[0].update()

    def update_date_siteform(self, new_date: datetime.datetime) -> None:
        self.newsite_form[0].controls[1].controls[2].value = new_date.strftime("%d/%m/%Y")
        self.newsite_form[0].controls[1].controls[2].update()

    def update_date_creditcardform(self, new_date: datetime.datetime) -> None:
        self.newcreditcard_form[0].controls[1].controls[4].value = new_date.strftime("%d/%m/%Y")
        self.newcreditcard_form[0].controls[1].controls[4].update()

    def update_date_noteform(self, new_date: datetime.datetime) -> None:
        self.newnote_form[0].controls[0].controls[2].value = new_date.strftime("%d/%m/%Y")
        self.newnote_form[0].controls[0].controls[2].update()

    def test01(self, _: ft.ControlEvent):
        value = self.newuser_form[0].controls[0].controls[0].value

        print(self.dropdown.value)
