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
    dangerTextColor,
    neutral00,
    neutral80,
    primaryTextColor,
    secondaryTextColor,
)


class AboutPage(ft.Row):
    """Displays app info and allows to send feedback."""
    def __init__(self, page: ft.Page, snackbar: Snackbar, update_changes: Callable[[], None]) -> None:
        super().__init__()

        # General attributes
        self.page = page
        self.snackbar = snackbar
        self.update_changes = update_changes
        self.span = ft.TextSpan(
            text="*",
            style=ft.TextStyle(font_family="AlbertSansB", color=dangerTextColor)
        )

        # About page attributes
        self.user: User = self.page.session.get("session")
        self.user_subject = CustomTextField(max_length=20)
        self.user_message = CustomTextField(min_lines=4, max_lines=4, max_length=500, on_submit=self.__submit_email)
        self.submit = CustomElevatedButton(
            name="Enviar",
            style=ButtonStyle.DEFAULT,
            on_click=self.__submit_email
        )

        # Design settings
        self.spacing = 32
        self.vertical_alignment = ft.CrossAxisAlignment.START

        # About content
        self.controls = [
            ft.Column(
                expand=True,
                spacing=32,
                controls=[

                    # App info
                    ft.Container(
                        expand=True,
                        bgcolor=neutral00,
                        border_radius=4,
                        padding=ft.padding.all(24),
                        shadow=ft.BoxShadow(
                            blur_radius=0.9,
                            offset=(0.0, 0.5),
                            color=ft.Colors.with_opacity(opacity=0.3, color=neutral80)
                        ),
                        content=ft.Row(
                            expand=True,
                            controls=[
                                ft.Column(
                                    spacing=24,
                                    expand=True,
                                    controls=[
                                        ft.Text(
                                            value="Dephokey — PasswordManager v.0.3.3",
                                            font_family="AlbertSansR",
                                            color=accentTextColor,
                                            size=20,
                                            no_wrap=True
                                        ),
                                        ft.Text(
                                            value="Password Manager es una aplicación que se encarga de almacenar "
                                                  "información sensible de forma encriptada y dentro de su propia "
                                                  "base de datos sin depender de una conexión a servidores de "
                                                  "terceros. Así se asegura de que las credenciales del usuario se "
                                                  "almacenen en su propio dispositivo, respetando su privacidad.",
                                            font_family="AlbertSansL",
                                            color=secondaryTextColor,
                                            size=16
                                        ),
                                        ft.Text(
                                            value="Joan Pastor Vicéns\nDephoKey © 2025",
                                            font_family="AlbertSansR",
                                            color=primaryTextColor,
                                            size=14
                                        ),
                                        ft.Column(
                                            spacing=8,
                                            controls=[
                                                ft.Text(
                                                    value="ADVERTENCIA",
                                                    font_family="AlbertSansB",
                                                    color=accentTextColor,
                                                    size=16
                                                ),
                                                ft.Text(
                                                    value="Hay que tener en cuenta que todos los datos almacenados no "
                                                          "deben de ser verídicos, pues dicha aplicación no cumple "
                                                          "con los estándares de seguridad PCI DSS. Esta aplicación "
                                                          "sólo es para la verificación del funcionamiento "
                                                          "establecido en el briefing del proyecto final.",
                                                    font_family="AlbertSansL",
                                                    color=secondaryTextColor,
                                                    size=16
                                                ),
                                                TextLink(
                                                    text="Más información",
                                                    target=lambda _: self.page.launch_url(
                                                        "https://stripe.com/es/guides/pci-compliance"
                                                    )
                                                ),
                                            ]
                                        ),
                                    ]
                                ),
                            ]
                        )
                    ),

                    # Feedback form
                    ft.Container(
                        expand=True,
                        bgcolor=neutral00,
                        border_radius=4,
                        padding=ft.padding.all(24),
                        shadow=ft.BoxShadow(
                            blur_radius=0.9,
                            offset=(0.0, 0.5),
                            color=ft.Colors.with_opacity(opacity=0.3, color=neutral80)
                        ),
                        content=ft.Row(
                            expand=True,
                            controls=[
                                ft.Column(
                                    spacing=24,
                                    expand=True,
                                    controls=[
                                        ft.Text(
                                            value="Ponte en contacto con nosotros",
                                            font_family="AlbertSansR",
                                            color=accentTextColor,
                                            size=20,
                                            no_wrap=True
                                        ),
                                        ft.Text(
                                            value="¿Alguna duda o problema? Rellena el siguiente formulario y nuestro "
                                                  "equipo se pondrá en contanto contigo lo más pronto posible:",
                                            font_family="AlbertSansL",
                                            color=secondaryTextColor,
                                            size=16
                                        ),
                                        ft.Column(
                                            spacing=8,
                                            controls=[
                                                ft.Text(
                                                    value="Motivo de la consulta",
                                                    font_family="AlbertSansR",
                                                    color=primaryTextColor,
                                                    spans=[self.span, ]
                                                ),
                                                self.user_subject,
                                            ]
                                        ),
                                        ft.Column(
                                            spacing=8,
                                            controls=[
                                                ft.Text(
                                                    value="Cuerpo del mensaje",
                                                    font_family="AlbertSansR",
                                                    spans=[self.span, ]
                                                ),
                                                self.user_message,
                                            ]
                                        ),
                                        self.submit,
                                    ]
                                ),
                            ]
                        )
                    ),
                ]
            ),
            ft.Column(
                expand=True,
                spacing=32,
                controls=[

                    # Technical Specifications
                    ft.Container(
                        expand=True,
                        bgcolor=neutral00,
                        border_radius=4,
                        padding=ft.padding.all(24),
                        shadow=ft.BoxShadow(
                            blur_radius=0.9,
                            offset=(0.0, 0.5),
                            color=ft.Colors.with_opacity(opacity=0.3, color=neutral80)
                        ),
                        content=ft.Row(
                            expand=True,
                            controls=[
                                ft.Column(
                                    spacing=24,
                                    expand=True,
                                    controls=[
                                        ft.Text(
                                            value="Más información",
                                            font_family="AlbertSansR",
                                            color=accentTextColor,
                                            size=20,
                                            no_wrap=True
                                        ),
                                        ft.Column(
                                            spacing=8,
                                            controls=[
                                                ft.Text(
                                                    value="Información técnica",
                                                    font_family="AlbertSansB",
                                                    color=accentTextColor,
                                                    size=16
                                                ),
                                                ft.Text(
                                                    value="Language Python 3.11.5: ",
                                                    font_family="AlbertSansB",
                                                    color=primaryTextColor,
                                                    size=16,
                                                    spans=[
                                                        ft.TextSpan(
                                                            text="Lenguaje de programación principal con el que ha "
                                                                 "creado el programa.",
                                                            style=ft.TextStyle(
                                                                font_family="AlbertSansR",
                                                                color=secondaryTextColor
                                                            )
                                                        ),
                                                    ]
                                                ),
                                                ft.Text(
                                                    value="Framework Flet 0.25.2: ",
                                                    font_family="AlbertSansB",
                                                    color=primaryTextColor,
                                                    size=16,
                                                    spans=[
                                                        ft.TextSpan(
                                                            text="Marco de trabajo que ha proporcionado las "
                                                                 "herramientas para la creación de toda la interfaz "
                                                                 "gráfica del programa.",
                                                            style=ft.TextStyle(
                                                                font_family="AlbertSansR",
                                                                color=secondaryTextColor
                                                            )
                                                        ),
                                                    ]
                                                ),
                                                ft.Text(
                                                    value="SQLAlchemy 2.0.36: ",
                                                    font_family="AlbertSansB",
                                                    color=primaryTextColor,
                                                    size=16,
                                                    spans=[
                                                        ft.TextSpan(
                                                            text="Mapedo objeto-relacional para la base de datos "
                                                                 "local que permite una comunicación y "
                                                                 "almacenamiento seguros.",
                                                            style=ft.TextStyle(
                                                                font_family="AlbertSansR",
                                                                color=secondaryTextColor
                                                            )
                                                        ),
                                                    ]
                                                ),
                                                ft.Text(
                                                    value="Cryptography 44.0.1: ", font_family="AlbertSansB",
                                                    color=primaryTextColor,
                                                    size=16,
                                                    spans=[
                                                        ft.TextSpan(
                                                            text="Encriptación mediante llaves de la información "
                                                                 "sensible de cada usuario registrado.",
                                                            style=ft.TextStyle(
                                                                font_family="AlbertSansR",
                                                                color=secondaryTextColor
                                                            )
                                                        ),
                                                    ]
                                                ),
                                            ]
                                        ),
                                        ft.Column(
                                            spacing=8,
                                            controls=[
                                                ft.Text(
                                                    value="Plataformas compatibles",
                                                    font_family="AlbertSansB",
                                                    color=accentTextColor,
                                                    size=16
                                                ),
                                                ft.Text(
                                                    value="Windows OS",
                                                    font_family="AlbertSansR",
                                                    color=secondaryTextColor,
                                                    size=16
                                                ),
                                            ]
                                        ),
                                        ft.Column(
                                            spacing=8,
                                            controls=[
                                                ft.Text(
                                                    value="Licencia",
                                                    font_family="AlbertSansB",
                                                    color=accentTextColor,
                                                    size=16
                                                ),
                                                ft.Text(
                                                    value="MIT | GPL 3.0",
                                                    font_family="AlbertSansR",
                                                    color=secondaryTextColor,
                                                    size=16
                                                ),
                                            ]
                                        ),
                                        ft.Column(
                                            spacing=8,
                                            controls=[
                                                ft.Text(
                                                    value="Agradecimientos",
                                                    font_family="AlbertSansB",
                                                    color=accentTextColor,
                                                    size=16
                                                ),
                                                ft.Text(
                                                    value="A Begoña por su acompañamiento a lo largo de este proceso. "
                                                          "Cuyo tiempo y dedicación empleados para la elección de la "
                                                          "paleta de color, los diseños de la interfaz y testeo de "
                                                          "la misma han sido de gran ayuda. Sin su paciencia, nada "
                                                          "de esto hubiera sido posible.\n¡Gracias!",
                                                    font_family="AlbertSansR",
                                                    color=secondaryTextColor,
                                                    size=16
                                                ),
                                            ]
                                        ),
                                        ft.Column(
                                            spacing=8,
                                            controls=[
                                                ft.Text(
                                                    value="Enlaces",
                                                    font_family="AlbertSansB",
                                                    color=accentTextColor,
                                                    size=16
                                                ),
                                                ft.Row(
                                                    spacing=8,
                                                    wrap=True,
                                                    controls=[
                                                        TextLink(
                                                            text="GitHub",
                                                            target=lambda _: self.page.launch_url(
                                                                "https://github.com/Ildiar25"
                                                            )
                                                        ),
                                                        ft.Text(
                                                            value="Mi perfil de programador. Ahí encontrarás todos mis "
                                                                  "trabajor realizados con mucho cariño.",
                                                            color=secondaryTextColor
                                                        ),
                                                    ]
                                                ),
                                                ft.Row(
                                                    spacing=8,
                                                    wrap=True,
                                                    controls=[
                                                        TextLink(
                                                            text="LinkedIn",
                                                            target=lambda _: self.page.launch_url(
                                                                "http://www.linkedin.com/in/"
                                                                "joan-pastor-vicens-aa5b4a55"
                                                            )
                                                        ),
                                                        ft.Text(
                                                            value="Mi perfil más profesional, donde podrás ver toda "
                                                                  "mi experiencia adquirida.",
                                                            color=secondaryTextColor
                                                        ),
                                                    ]
                                                ),
                                            ]
                                        ),
                                    ]
                                ),
                            ]
                        )
                    ),
                ]
            ),
        ]

    def update_content(self) -> None:
        # WARNING: 'update_content()' is a ContentManager dependency. However, since this page does not require to be
        # content updates, this function is implemented as a no-op.
        pass

    def __submit_email(self, _: ft.ControlEvent) -> None:
        reason = self.user_subject.value.strip().capitalize()
        message = self.user_message.value.strip()

        if not reason:
            self.user_message.reset_error()
            self.user_message.update()
            self.user_subject.show_error("¡Debes indicar un motivo!")
            self.user_subject.update()
            return

        if not message:
            self.user_subject.reset_error()
            self.user_subject.update()
            self.user_message.show_error("El contenido del mensaje debe rellenarse")
            self.user_message.update()
            return

        self.__send_coments(reason=reason, message=message)
        self.__reset_fields()

    def __send_coments(self, reason: str, message: str) -> None:
        new_email = SendEmail(
            msg_style=MessageStyle.QUERY,
            send_from=self.user.email,
            subject=reason,
            content=message
        )

        if not new_email.send():
            self.__display_message(
                msg="Ha habido un problema durante el envío del mensaje.\nContacta con el Soporte Técnico",
                style=SnackbarStyle.DANGER
            )
            return

        self.__display_message(
            msg="¡Gracias por tus comentarios!\nTrabajaremos lo más rápido posible para hacerte llegar una respuesta.",
            style=SnackbarStyle.SUCCESS
        )

    def __reset_fields(self) -> None:
        self.user_message.value = ""
        self.user_message.reset_error()
        self.user_message.update()
        self.user_subject.value = ""
        self.user_subject.reset_error()
        self.user_subject.update()

    def __display_message(self, msg: str, style: SnackbarStyle) -> None:
        self.snackbar.change_style(msg=msg, style=style)
        self.snackbar.update()
