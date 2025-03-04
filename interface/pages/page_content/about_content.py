import flet as ft
from typing import Callable

from features.models.user import User

from interface.controls import Snackbar, CustomTextField, CustomElevatedButton, ButtonStyle

from shared.utils.colors import *


class AboutPage(ft.Row):
    def __init__(self, page: ft.Page, snackbar: Snackbar, update_changes: Callable[[], None]) -> None:
        super().__init__()

        # General attributes
        self.page = page
        self.snackbar = snackbar
        self.update_changes = update_changes

        # About attributes
        self.user: User = self.page.session.get("session")
        self.reason = CustomTextField(max_length=20)
        self.body_message = CustomTextField(min_lines=4, max_lines=4)
        self.span = ft.TextSpan(text="*", style=ft.TextStyle(font_family="AlbertSansB", color=dangerTextColor))
        self.submit = CustomElevatedButton(name="Enviar", style=ButtonStyle.DEFAULT)

        # Design settings
        self.spacing = 32
        self.vertical_alignment = ft.CrossAxisAlignment.START

        # About content
        self.controls = [
            ft.Row(
                vertical_alignment=ft.CrossAxisAlignment.START,
                spacing=32,
                expand=True,
                controls=[
                    ft.Column(
                        expand=True,
                        spacing=32,
                        controls=[
                            # App info
                            ft.Container(
                                expand=True,
                                bgcolor=bgGeneralFormColor,
                                border_radius=4,
                                padding=ft.padding.all(24),
                                shadow=ft.BoxShadow(
                                    blur_radius=0.9, offset=(0.0, 0.5),
                                    color=ft.Colors.with_opacity(opacity=0.3, color=neutral80)
                                ),
                                content=ft.Column(
                                    horizontal_alignment=ft.CrossAxisAlignment.END,
                                    spacing=24,
                                    controls=[
                                        ft.Row(
                                            controls=[
                                                ft.Text(value="Dephokey — PasswordManager v.0.3.3",
                                                        font_family="AlbertSansR",
                                                        color=accentTextColor, size=20, no_wrap=True)
                                            ]
                                        ),
                                        ft.Text(value="Password Manager es una aplicación que se encarga de almacenar "
                                                      "información sensible de forma encriptada dentro de su propia "
                                                      "base de datos, sin conexión a servidores de terceros. "
                                                      "Asegurando así que el usuario tenga sus credenciales bajo su "
                                                      "techo y respetando la privacidad del mismo.",
                                                font_family="AlbertSansL", color=primaryTextColor, size=16),
                                        ft.Text(value="Joan Pastor Vicéns\nDephoKey © 2025",
                                                font_family="AlbertSansR", color=primaryTextColor, size=16)
                                    ]
                                )
                            ),

                            # Feedback form
                            ft.Container(
                                expand=True,
                                bgcolor=bgGeneralFormColor,
                                border_radius=4,
                                padding=ft.padding.all(24),
                                shadow=ft.BoxShadow(
                                    blur_radius=0.9, offset=(0.0, 0.5),
                                    color=ft.Colors.with_opacity(opacity=0.3, color=neutral80)
                                ),
                                content=ft.Column(
                                    horizontal_alignment=ft.CrossAxisAlignment.END,
                                    spacing=24,
                                    controls=[
                                        ft.Row(
                                            controls=[
                                                ft.Text(value="Ponte en contacto con nosotros",
                                                        font_family="AlbertSansR",
                                                        color=accentTextColor, size=20, no_wrap=True)
                                            ]
                                        ),
                                        ft.Text(value="¿Alguna duda o problema? Rellena el siguiente formulario y "
                                                      "nuestro equipo se pondrá en contacto contigo:",
                                                font_family="AlbertSansL", color=primaryTextColor, size=16),
                                        ft.Column(
                                            spacing=16,
                                            controls=[
                                                ft.Column(
                                                    spacing=8,
                                                    controls=[
                                                        ft.Text(value="Motivo de la consulta",
                                                                font_family="AlbertSansR", spans=[self.span]),
                                                        self.reason
                                                    ]
                                                ),
                                                ft.Column(
                                                    spacing=8,
                                                    controls=[
                                                        ft.Text(value="Cuerpo del mensaje",
                                                                font_family="AlbertSansR", spans=[self.span]),
                                                        self.body_message
                                                    ]
                                                )
                                            ]
                                        ),
                                        self.submit
                                    ]
                                )
                            )
                        ]
                    ),
                    ft.Column(
                        expand=True,
                        controls=[

                            # Technical info
                            ft.Container(
                                expand=True,
                                bgcolor=bgGeneralFormColor,
                                border_radius=4,
                                padding=ft.padding.all(24),
                                shadow=ft.BoxShadow(
                                    blur_radius=0.9, offset=(0.0, 0.5),
                                    color=ft.Colors.with_opacity(opacity=0.3, color=neutral80)
                                ),
                                content=ft.Column(
                                    spacing=24,
                                    controls=[
                                        ft.Text(value="Más información", font_family="AlbertSansR",
                                                color=accentTextColor, size=20, no_wrap=True),
                                        ft.Column(
                                            spacing=16,
                                            controls=[

                                            ]
                                        )
                                    ]
                                )
                            )
                        ]
                    )
                ]
            )
        ]

        self.update_content()

    def update_content(self) -> None:
        pass
