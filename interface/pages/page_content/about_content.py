from collections.abc import Callable

import flet as ft

from features.email_management.create_message import MessageStyle
from features.email_management.send_email import SendEmail
from features.models.user import User
from interface.controls import CustomElevatedButton, CustomTextField, TextLink
from interface.controls.e_button import ButtonStyle
from interface.controls.snackbar import Snackbar, SnackbarStyle
from shared.utils.colors import (
    accentTextColor,
    bgGeneralFormColor,
    dangerTextColor,
    neutral80,
    primaryTextColor,
    secondaryTextColor,
)


class AboutPage(ft.Row):
    def __init__(self, page: ft.Page, snackbar: Snackbar, update_changes: Callable[[], None]) -> None:
        super().__init__()

        # General attributes
        self.page = page
        self.snackbar = snackbar
        self.update_changes = update_changes

        # About attributes
        self.user: User = self.page.session.get("session")
        self.query_reason = CustomTextField(max_length=20)
        self.body_message = CustomTextField(min_lines=4, max_lines=4, max_length=500)

        self.span = ft.TextSpan(text="*", style=ft.TextStyle(font_family="AlbertSansB", color=dangerTextColor))
        self.submit = CustomElevatedButton(name="Enviar", style=ButtonStyle.DEFAULT, on_click=self.__submit_email)

        # Design settings
        self.spacing = 32
        self.vertical_alignment = ft.CrossAxisAlignment.START

        self.controls = [
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
                        content=ft.Row(
                            expand=True,
                            controls=[
                                ft.Column(
                                    spacing=24,
                                    expand=True,
                                    controls=[
                                        ft.Text(value="Dephokey — PasswordManager v.0.3.3", font_family="AlbertSansR",
                                                color=accentTextColor, size=20, no_wrap=True),
                                        ft.Text(value="Password Manager es una aplicación que se encarga de almacenar "
                                                      "información sensible de forma encriptada y dentro de su propia "
                                                      "base de datos sin depender de una conexión a servidores de "
                                                      "terceros. Así se asegura de que las credenciales del usuario se "
                                                      "almacenen en su propio dispositivo, respetando su privacidad.",
                                                font_family="AlbertSansL", color=secondaryTextColor, size=16),
                                        ft.Text(value="Joan Pastor Vicéns\nDephoKey © 2025",
                                                font_family="AlbertSansR", color=primaryTextColor, size=14)
                                    ]
                                )
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
                        content=ft.Row(
                            expand=True,
                            controls=[
                                ft.Column(
                                    spacing=24,
                                    expand=True,
                                    controls=[
                                        ft.Text(value="Ponte en contacto con nosotros", font_family="AlbertSansR",
                                                color=accentTextColor, size=20, no_wrap=True),
                                        ft.Text(value="¿Alguna duda o problema? Rellena el siguiente formulario y "
                                                      "nuestro equipo se pondrá en contanto contigo lo más pronto "
                                                      "posible:",
                                                font_family="AlbertSansL", color=secondaryTextColor, size=16),
                                        ft.Column(
                                            spacing=8,
                                            controls=[
                                                ft.Text(value="Motivo de la consulta", font_family="AlbertSansR",
                                                        color=primaryTextColor, spans=[self.span]),
                                                self.query_reason
                                            ]),
                                        ft.Column(
                                            spacing=8,
                                            controls=[
                                                ft.Text(value="Cuerpo del mensaje", font_family="AlbertSansR",
                                                        color=primaryTextColor, spans=[self.span]),
                                                self.body_message
                                            ]),
                                        self.submit
                                    ]
                                )
                            ]
                        )
                    )
                ]
            ),
            ft.Column(
                expand=True,
                spacing=32,
                controls=[
                    # Technical Specifications
                    ft.Container(
                        expand=True,
                        bgcolor=bgGeneralFormColor,
                        border_radius=4,
                        padding=ft.padding.all(24),
                        shadow=ft.BoxShadow(
                            blur_radius=0.9, offset=(0.0, 0.5),
                            color=ft.Colors.with_opacity(opacity=0.3, color=neutral80)
                        ),
                        content=ft.Row(
                            expand=True,
                            controls=[
                                ft.Column(
                                    spacing=24,
                                    expand=True,
                                    controls=[
                                        ft.Text(value="Más información", font_family="AlbertSansR",
                                                color=accentTextColor, size=20, no_wrap=True),
                                        ft.Column(
                                            spacing=8,
                                            controls=[
                                                ft.Text(value="Información técnica", font_family="AlbertSansB",
                                                        color=accentTextColor, size=16),
                                                ft.Text(value="Language Python 3.11.5: ", font_family="AlbertSansB",
                                                        color=primaryTextColor, size=16,
                                                        spans=[
                                                            ft.TextSpan(text="Lenguaje de programación principal con "
                                                                             "el que ha creado el programa.",
                                                                        style=ft.TextStyle(
                                                                            font_family="AlbertSansR",
                                                                            color=secondaryTextColor
                                                                        ))
                                                        ]),
                                                ft.Text(value="Framework Flet 0.25.2: ", font_family="AlbertSansB",
                                                        color=primaryTextColor, size=16,
                                                        spans=[
                                                            ft.TextSpan(text="Marco de trabajo que ha proporcionado "
                                                                             "las herramientas para la creación de "
                                                                             "toda la interfaz gráfica del programa.",
                                                                        style=ft.TextStyle(
                                                                            font_family="AlbertSansR",
                                                                            color=secondaryTextColor
                                                                        ))
                                                        ]),
                                                ft.Text(value="SQLAlchemy 2.0.36: ", font_family="AlbertSansB",
                                                        color=primaryTextColor, size=16,
                                                        spans=[
                                                            ft.TextSpan(text="Mapedo objeto-relacional para la base "
                                                                             "de datos local que permite una "
                                                                             "comunicación y almacenamiento seguros.",
                                                                        style=ft.TextStyle(
                                                                            font_family="AlbertSansR",
                                                                            color=secondaryTextColor
                                                                        ))
                                                        ]),
                                                ft.Text(value="Cryptography 44.0.1: ", font_family="AlbertSansB",
                                                        color=primaryTextColor, size=16,
                                                        spans=[
                                                            ft.TextSpan(text="Encriptación mediante llaves de la "
                                                                             "información sensible de cada usuario "
                                                                             "registrado.",
                                                                        style=ft.TextStyle(
                                                                            font_family="AlbertSansR",
                                                                            color=secondaryTextColor
                                                                        ))
                                                        ]),
                                            ]
                                        ),
                                        ft.Column(
                                            spacing=8,
                                            controls=[
                                                ft.Text(value="Plataformas compatibles", font_family="AlbertSansB",
                                                        color=accentTextColor, size=16),
                                                ft.Text(value="Windows OS", font_family="AlbertSansR",
                                                        color=secondaryTextColor, size=16)
                                            ]
                                        ),
                                        ft.Column(
                                            spacing=8,
                                            controls=[
                                                ft.Text(value="Licencia", font_family="AlbertSansB",
                                                        color=accentTextColor, size=16),
                                                ft.Text(value="MIT | GPL 3.0", font_family="AlbertSansR",
                                                        color=secondaryTextColor, size=16)
                                            ]
                                        ),
                                        ft.Column(
                                            spacing=8,
                                            controls=[
                                                ft.Text(value="Agradecimientos", font_family="AlbertSansB",
                                                        color=accentTextColor, size=16),
                                                ft.Text(value="A Begoña por su acompañamiento a lo largo de este "
                                                              "proceso. Cuyo tiempo y dedicación empleados para la "
                                                              "elección de la paleta de color, los diseños de la "
                                                              "interfaz y testeo de la misma han sido de gran ayuda. "
                                                              "Sin su paciencia, nada de esto hubiera sido posible.\n"
                                                              "¡Gracias!",
                                                        font_family="AlbertSansR", color=secondaryTextColor, size=16)
                                            ]
                                        ),
                                        ft.Column(
                                            spacing=8,
                                            controls=[
                                                ft.Text(value="Enlaces", font_family="AlbertSansB",
                                                        color=accentTextColor, size=16),
                                                ft.Row(
                                                    spacing=8,
                                                    wrap=True,
                                                    controls=[
                                                        TextLink(
                                                            text="GitHub", function=lambda _: self.page.launch_url(
                                                                "https://github.com/Ildiar25"
                                                            )
                                                        ),
                                                        ft.Text(
                                                            value="Mi perfil de programador. Ahí encontrarás todos mis "
                                                                  "trabajor realizados con mucho cariño.",
                                                            color=secondaryTextColor
                                                        )
                                                    ]
                                                ),
                                                ft.Row(
                                                    spacing=8,
                                                    wrap=True,
                                                    controls=[
                                                        TextLink(
                                                            text="LinkedIn", function=lambda _: self.page.launch_url(
                                                                "http://www.linkedin.com/in/joan-pastor-vicens-aa5b4a55"
                                                            )
                                                        ),
                                                        ft.Text(
                                                            value="Mi perfil más profesional, donde podrás ver toda "
                                                                  "mi experiencia adquirida.",
                                                            color=secondaryTextColor
                                                        )
                                                    ]
                                                )
                                            ]
                                        )
                                    ]
                                )
                            ]
                        )
                    )
                ]
            )
        ]

    def update_content(self) -> None:
        # Content manager needs this function to work with. However, this page doesn't need to be updated so this
        # function needs to be ignored.
        pass

    def __submit_email(self, _: ft.ControlEvent) -> None:
        reason = self.query_reason.value.strip().capitalize()
        message = self.body_message.value.strip()

        if not reason:
            self.body_message.reset_error()
            self.body_message.update()
            self.query_reason.show_error("¡Debes indicar un motivo!")
            self.query_reason.update()
            return

        if not message:
            self.query_reason.reset_error()
            self.query_reason.update()
            self.body_message.show_error("El contenido del mensaje debe rellenarse")
            self.body_message.update()
            return

        self.body_message.reset_error()
        self.body_message.update()
        self.query_reason.reset_error()
        self.query_reason.update()

        new_email = SendEmail(
            msg_style=MessageStyle.QUERY,
            send_from=self.user.email,
            subject=reason,
            content=message
        )

        if not new_email.send():
            self.snackbar.change_style(
                msg="Ha habido un problema durante el envío del mensaje.\nContacta con el Servicio de Asistencia",
                style=SnackbarStyle.DANGER)
            self.snackbar.update()
            return

        self.query_reason.value = ""
        self.query_reason.update()
        self.body_message.value = ""
        self.body_message.update()

        self.snackbar.change_style(
            msg="¡Gracias por tus comentarios!\nTrabajaremos lo más rápido posible para hacerte llegar los resultados.",
            style=SnackbarStyle.SUCCESS)
        self.snackbar.update()
