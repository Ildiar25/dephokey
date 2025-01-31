import flet as ft

from interface.controls import CustomTextField, CustomElevatedButton

from shared.utils.colors import *


class Admin(ft.Column):
    def __init__(self, page: ft.Page) -> None:
        super().__init__()

        # General attributes
        self.page = page
        self.main_content = None
        self.submit_button = CustomElevatedButton(
            name="Añadir", expand=True
        )

        #Admin attributes
        self.submit_user = CustomElevatedButton(
            name="Añadir Usuario", expand=True, icon=ft.Icons.ADD_ROUNDED, foreground_color=tertiaryTextColor,
            bg_color=primaryCorporateColor, border_size=-1, on_click=self.test01)
        self.submit_site = CustomElevatedButton(
            name="Añadir Dirección", expand=True, icon=ft.Icons.ADD_ROUNDED, foreground_color=tertiaryTextColor,
            bg_color=primaryCorporateColor, border_size=-1)
        self.submit_creditcard = CustomElevatedButton(
            name="Añadir Tarjeta", expand=True, icon=ft.Icons.ADD_ROUNDED, foreground_color=tertiaryTextColor,
            bg_color=primaryCorporateColor, border_size=-1)
        self.submit_note = CustomElevatedButton(
            name="Añadir Nota", expand=True, icon=ft.Icons.ADD_ROUNDED, foreground_color=tertiaryTextColor,
            bg_color=primaryCorporateColor, border_size=-1)

        # Forms
        self.newuser_form = [
            ft.Column(
                spacing=22,
                controls=[
                    ft.Row(
                        controls=[
                            CustomTextField(label="Nombre completo", expand=True),
                            CustomTextField(label="Correo electrónico", expand=True),
                            CustomTextField(label="Contraseña", expand=True),
                        ]
                    ),
                    ft.Row(),
                    ft.Row(
                        controls=[
                            self.submit_user
                        ]
                    )
                ]
            )
        ]
        self.newsite_form = [
            ft.Column(
                spacing=22,
                controls=[
                    ft.Row(),
                    ft.Row(),
                    ft.Row(),
                ]
            )
        ]
        self.newcreditcard_form = [
            ft.Column(
                spacing=22,
                controls=[
                    ft.Row(),
                    ft.Row(),
                    ft.Row(),
                ]
            )
        ]
        self.newnote_form = [
            ft.Column(
                spacing=22,
                controls=[
                    ft.Row(),
                    ft.Row(),
                    ft.Row(),
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
                    title=ft.Text(value="Añadir Usuario", font_family="AlbertSansR", size=20, color=accentTextColor),
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
                    title=ft.Text(value="Añadir Dirección Web", font_family="AlbertSansR", size=20,
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
                    title=ft.Text(value="Añadir Tarjeta de Crédito", font_family="AlbertSansR", size=20,
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
                    title=ft.Text(value="Añadir Nota Segura", font_family="AlbertSansR", size=20,
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

    def test01(self, _: ft.ControlEvent):
        value = self.newuser_form[0].controls[0].controls[0].value
        print(value)
