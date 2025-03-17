import flet as ft
from typing import Callable, List
from datetime import datetime

from data.db_orm import session

from features.models.user import User, UserRole
from features.models import *

from interface.controls import Snackbar, CustomTextField, CustomSwitch, CustomElevatedButton, ButtonStyle, SnackbarStyle
from interface.pages.widgets import AdminRow, RowStyle

from shared.validate import Validate
from shared.utils.colors import *


class AdminPage(ft.Column):
    def __init__(self, page: ft.Page, snackbar: Snackbar, update_changes: Callable[[], None]) -> None:
        super().__init__()

        # General attributes
        self.page = page
        self.snackbar = snackbar
        self.update_changes = update_changes

        # Admin attributes
        self.users: List[User] = []
        self.sites: List[Site] = []
        self.creditcards: List[CreditCard] = []
        self.notes: List[Note] = []
        self.pass_requests: List[PasswordRequest] = []
        self.span = ft.TextSpan(text="*", style=ft.TextStyle(font_family="AlbertSansB", color=dangerTextColor))
        self.site_dropdown = ft.Dropdown(
            label="Selecciona un correo",
            expand=True,
            label_style=ft.TextStyle(color=secondaryTextColor),
            select_icon=ft.Icons.KEYBOARD_ARROW_DOWN_ROUNDED,
            icon_enabled_color=primaryCorporateColor,
            bgcolor=bgGeneralFormColor,
            border_color=neutral20,
            focused_border_color=primaryCorporateColor,
            border_radius=4,
        )
        self.creditcard_dropdown = ft.Dropdown(
            label="Selecciona un correo",
            expand=True,
            label_style=ft.TextStyle(color=secondaryTextColor),
            select_icon=ft.Icons.KEYBOARD_ARROW_DOWN_ROUNDED,
            icon_enabled_color=primaryCorporateColor,
            bgcolor=bgGeneralFormColor,
            border_color=neutral20,
            focused_border_color=primaryCorporateColor,
            border_radius=4,
        )
        self.note_dropdown = ft.Dropdown(
            label="Selecciona un correo",
            expand=True,
            label_style=ft.TextStyle(color=secondaryTextColor),
            select_icon=ft.Icons.KEYBOARD_ARROW_DOWN_ROUNDED,
            icon_enabled_color=primaryCorporateColor,
            bgcolor=bgGeneralFormColor,
            border_color=neutral20,
            focused_border_color=primaryCorporateColor,
            border_radius=4,
        )

        # Admin Userform attributes
        self.u_fullname = CustomTextField(hint_text="Introduce el nombre completo del usuario", max_length=150)
        self.u_email = CustomTextField(hint_text="Añade su dirección de correo", max_length=50)
        self.u_password = CustomTextField(
            hint_text="Incluye una contraseña segura", max_length=50, password=True, can_reveal_password=True
        )
        self.u_switch = CustomSwitch(title="Selecciona si el usuario es ADMIN")
        self.u_submit = CustomElevatedButton(name="Añadir usuario", style=ButtonStyle.ICON, on_click=self.add_new_user)

        self.s_name = CustomTextField(hint_text="Dale un nombre a la dirección",max_length=30)
        self.s_address = CustomTextField(hint_text="Escribe la dirección", max_length=50, prefix_text="http://")
        self.s_username = CustomTextField(hint_text="Añade el usuario con el que te has registrado", max_length=30)
        self.s_password = CustomTextField(
            hint_text="Escribe la contraseña", max_length=30, password=True, can_reveal_password=True
        )
        self.s_submit = CustomElevatedButton(name="Añadir sitio", style=ButtonStyle.ICON, on_click=self.add_new_site)

        self.cc_alias = CustomTextField(hint_text="Agrega un alias", max_length=30)
        self.cc_holder = CustomTextField(hint_text="Introduce el nombre del titular", max_length=30)
        self.cc_number = CustomTextField(
            hint_text="Añade el número de tarjeta", can_reveal_password=True,max_length=19, password=True,
            input_filter=ft.NumbersOnlyInputFilter()
        )
        self.cc_cvc = CustomTextField(
            hint_text="cvc", width=104, password=True, can_reveal_password=True, max_length=4,
            input_filter=ft.NumbersOnlyInputFilter()
        )
        self.cc_date = CustomTextField(hint_text="mm/yy", max_length=5)
        self.cc_submit = CustomElevatedButton(name="Añadir tarjeta", style=ButtonStyle.ICON,
                                              on_click=self.add_new_creditcard)

        self.n_title = CustomTextField(hint_text="Añade un título", max_length=25)
        self.n_content = CustomTextField(
            hint_text="Agrega contenido importante", can_reveal_password=True,
            password=True, max_lines=4, min_lines=4, max_length=324
        )
        self.n_submit = CustomElevatedButton(name="Añadir nota", style=ButtonStyle.ICON, on_click=self.add_new_note)

        # Body content
        self.user_rows = ft.Column()
        self.site_rows = ft.Column()
        self.creditcard_rows = ft.Column()
        self.note_rows = ft.Column()
        self.pass_request_rows = ft.Column()

        # Admin Forms
        self.user_form = ft.Container(
            height=600,
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
                        expand=True,
                        spacing=16,
                        controls=[
                            ft.Row(controls=[
                                ft.Text(value="Añadir usuario", font_family="AlbertSansR",
                                        size=18, color=accentTextColor),
                            ]),
                            ft.Column(spacing=8, controls=[
                                ft.Text(value="Nombre completo", font_family="AlbertSansR",
                                        color=primaryTextColor, spans=[self.span]),
                                self.u_fullname
                            ]),
                            ft.Column(spacing=8, controls=[
                                ft.Text(value="Correo electrónico", font_family="AlbertSansR",
                                        color=primaryTextColor, spans=[self.span]),
                                self.u_email
                            ]),
                            ft.Column(spacing=8, controls=[
                                ft.Text(value="Contraseña", font_family="AlbertSansR",
                                        color=primaryTextColor, spans=[self.span]),
                                self.u_password
                            ]),
                            self.u_switch,
                            ft.Column(expand=True),
                            ft.Row(controls=[self.u_submit], alignment=ft.MainAxisAlignment.END)
                        ]
                    )
                ]
            )
        )
        self.site_form = ft.Container(
            height=600,
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
                        expand=True,
                        spacing=16,
                        controls=[
                            ft.Row(controls=[
                                ft.Text(value="Añadir sitio web", font_family="AlbertSansR",
                                        size=18, color=accentTextColor),
                            ]),
                            ft.Column(spacing=8, controls=[
                                ft.Text(value="Usuario asociado", font_family="AlbertSansR",
                                        color=primaryTextColor, spans=[self.span]),
                                self.site_dropdown
                            ]),
                            ft.Column(spacing=8, controls=[
                                ft.Text(value="Nombre del sitio", font_family="AlbertSansR",
                                        color=primaryTextColor, spans=[]),
                                self.s_name
                            ]),
                            ft.Column(spacing=8, controls=[
                                ft.Text(value="Dirección web", font_family="AlbertSansR",
                                        color=primaryTextColor, spans=[self.span]),
                                self.s_address
                            ]),
                            ft.Column(spacing=8, controls=[
                                ft.Text(value="Nombre de usuario", font_family="AlbertSansR",
                                        color=primaryTextColor, spans=[self.span]),
                                self.s_username
                            ]),
                            ft.Column(spacing=8, controls=[
                                ft.Text(value="Contraseña", font_family="AlbertSansR",
                                        color=primaryTextColor, spans=[self.span]),
                                self.s_password
                            ]),
                            ft.Column(expand=True),
                            ft.Row(controls=[self.s_submit], alignment=ft.MainAxisAlignment.END)
                        ]
                    )
                ]
            )
        )
        self.creditcard_form = ft.Container(
            height=600,
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
                        expand=True,
                        spacing=16,
                        controls=[
                            ft.Row(controls=[
                                ft.Text(value="Añadir tarjeta de crédito", font_family="AlbertSansR",
                                        size=18, color=accentTextColor),
                            ]),
                            ft.Column(spacing=8, controls=[
                                ft.Text(value="Usuario asociado", font_family="AlbertSansR",
                                        color=primaryTextColor, spans=[self.span]),
                                self.creditcard_dropdown
                            ]),
                            ft.Column(spacing=8, controls=[
                                ft.Text(value="Alias", font_family="AlbertSansR", color=primaryTextColor),
                                self.cc_alias
                            ]),
                            ft.Column(spacing=8, controls=[
                                ft.Text(value="Nombre del titular", font_family="AlbertSansR", color=primaryTextColor),
                                self.cc_number
                            ]),
                            ft.Column(spacing=8, controls=[
                                ft.Text(value="Número de la tarjeta", font_family="AlbertSansR",
                                        color=primaryTextColor, spans=[self.span]),
                                self.cc_number
                            ]),
                            ft.Row(spacing=16, alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                                ft.Column(spacing=8, expand=True, controls=[
                                    ft.Text(value="Fecha de validez", font_family="AlbertSansR",
                                            color=primaryTextColor, spans=[self.span]),
                                    self.cc_date
                                ]),
                                ft.VerticalDivider(),
                                ft.Column(spacing=8, controls=[
                                    ft.Text(value="CVC", font_family="AlbertSansR",
                                            color=primaryTextColor, spans=[self.span]),
                                    self.cc_cvc
                                ]),
                            ]),
                            ft.Column(expand=True),
                            ft.Row(controls=[self.cc_submit], alignment=ft.MainAxisAlignment.END)
                        ]
                    )
                ]
            )
        )
        self.note_form = ft.Container(
            height=600,
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
                        expand=True,
                        spacing=16,
                        controls=[
                            ft.Row(controls=[
                                ft.Text(value="Añadir nota segura", font_family="AlbertSansR",
                                        size=18, color=accentTextColor),
                            ]),
                            ft.Column(spacing=8, controls=[
                                ft.Text(value="Usuario asociado", font_family="AlbertSansR",
                                        color=primaryTextColor, spans=[self.span]),
                                self.note_dropdown
                            ]),
                            ft.Column(spacing=8, controls=[
                                ft.Text(value="Título de la nota", font_family="AlbertSansR",
                                        color=primaryTextColor, spans=[]),
                                self.n_title
                            ]),
                            ft.Column(spacing=8, controls=[
                                ft.Text(value="Contenido", font_family="AlbertSansR",
                                        color=primaryTextColor, spans=[self.span]),
                                self.n_content
                            ]),
                            ft.Column(expand=True),
                            ft.Row(controls=[self.n_submit], alignment=ft.MainAxisAlignment.END)
                        ]
                    )
                ]
            )
        )

        self.all_users = ft.Container(
            expand=True,
            bgcolor=bgGeneralFormColor,
            border_radius=4,
            shadow=ft.BoxShadow(
                blur_radius=0.9, offset=(0.0, 0.5),
                color=ft.Colors.with_opacity(opacity=0.3, color=neutral80)
            ),
            content=ft.ExpansionTile(
                title=ft.Text(value="Usuarios", size=20, color=accentTextColor),
                controls_padding=ft.padding.all(22),
                shape=ft.RoundedRectangleBorder(4),
                collapsed_shape=ft.RoundedRectangleBorder(4),
                min_tile_height=44,
                bgcolor=bgGeneralFormColor,
                collapsed_bgcolor=bgGeneralFormColor,
                controls=[self.user_rows]
            )
        )
        self.all_sites = ft.Container(
            expand=True,
            bgcolor=bgGeneralFormColor,
            border_radius=4,
            shadow=ft.BoxShadow(
                blur_radius=0.9, offset=(0.0, 0.5),
                color=ft.Colors.with_opacity(opacity=0.3, color=neutral80)
            ),
            content=ft.ExpansionTile(
                title=ft.Text(value="Sitios web", size=20, color=accentTextColor),
                controls_padding=ft.padding.all(22),
                shape=ft.RoundedRectangleBorder(4),
                collapsed_shape=ft.RoundedRectangleBorder(4),
                min_tile_height=44,
                bgcolor=bgGeneralFormColor,
                collapsed_bgcolor=bgGeneralFormColor,
                controls=[self.site_rows]
            )
        )
        self.all_creditcards = ft.Container(
            expand=True,
            bgcolor=bgGeneralFormColor,
            border_radius=4,
            shadow=ft.BoxShadow(
                blur_radius=0.9, offset=(0.0, 0.5),
                color=ft.Colors.with_opacity(opacity=0.3, color=neutral80)
            ),
            content=ft.ExpansionTile(
                title=ft.Text(value="Tarjetas de crédito", size=20, color=accentTextColor),
                controls_padding=ft.padding.all(22),
                shape=ft.RoundedRectangleBorder(4),
                collapsed_shape=ft.RoundedRectangleBorder(4),
                min_tile_height=44,
                bgcolor=bgGeneralFormColor,
                collapsed_bgcolor=bgGeneralFormColor,
                controls=[self.creditcard_rows]
            )
        )
        self.all_notes = ft.Container(
            expand=True,
            bgcolor=bgGeneralFormColor,
            border_radius=4,
            shadow=ft.BoxShadow(
                blur_radius=0.9, offset=(0.0, 0.5),
                color=ft.Colors.with_opacity(opacity=0.3, color=neutral80)
            ),
            content=ft.ExpansionTile(
                title=ft.Text(value="Notas seguras", size=20, color=accentTextColor),
                controls_padding=ft.padding.all(22),
                shape=ft.RoundedRectangleBorder(4),
                collapsed_shape=ft.RoundedRectangleBorder(4),
                min_tile_height=44,
                bgcolor=bgGeneralFormColor,
                collapsed_bgcolor=bgGeneralFormColor,
                controls=[self.note_rows]
            )
        )
        self.all_requests = ft.Container(
            expand=True,
            bgcolor=bgGeneralFormColor,
            border_radius=4,
            shadow=ft.BoxShadow(
                blur_radius=0.9, offset=(0.0, 0.5),
                color=ft.Colors.with_opacity(opacity=0.3, color=neutral80)
            ),
            content=ft.ExpansionTile(
                title=ft.Text(value="Peticiones de cambio de contraseña", size=20, color=accentTextColor),
                controls_padding=ft.padding.all(22),
                shape=ft.RoundedRectangleBorder(4),
                collapsed_shape=ft.RoundedRectangleBorder(4),
                min_tile_height=44,
                bgcolor=bgGeneralFormColor,
                collapsed_bgcolor=bgGeneralFormColor,
                controls=[self.pass_request_rows]
            )
        )

        # Design settings
        self.espacing = 32

        self.controls = [
            ft.Row(
                expand=True,
                spacing=32,
                controls=[
                    ft.Column(
                        expand=True,
                        spacing=24,
                        controls=[
                            # New User form
                            self.user_form,
                            # New Creditcard form
                            self.creditcard_form
                        ]
                    ),
                    ft.Column(
                        expand=True,
                        spacing=24,
                        controls=[
                            # New Site form
                            self.site_form,
                            # New Note form
                            self.note_form
                        ]
                    ),
                ]
            ),
            ft.Divider(),
            self.all_users,
            self.all_sites,
            self.all_creditcards,
            self.all_notes,
            self.all_requests
        ]

        self.update_content()

    def add_new_user(self, _: ft.ControlEvent) -> None:
        self.u_fullname.reset_error()
        self.u_email.reset_error()
        self.u_password.reset_error()

        fullname = self.u_fullname.value.strip().title()
        email = self.u_email.value.strip().lower()
        password = self.u_password.value.strip()
        role = UserRole.ADMIN if self.u_switch.get_value() else UserRole.CLIENT

        # Validate fields
        if not fullname:
            self.u_fullname.show_error("¡El usuario debe tener un nombre!")
            return

        if not Validate.is_valid_email(email):
            self.u_email.show_error("¡Se necesita un correo electrónico válido!")
            return

        if not Validate.is_valid_password(password):
            self.u_password.show_error("¡La contraseña necesita números, mayúsculas y minúsculas")
            return

        self.u_fullname.reset_error()
        self.u_email.reset_error()
        self.u_password.reset_error()

        # New user instance
        user = User(fullname, email, password, role)
        session.add(user)
        session.commit()

        # Reset fields
        self.u_fullname.value = ""
        self.u_email.value = ""
        self.u_password.value = ""
        self.u_switch.set_value(False)
        self.user_form.update()

        # Show & update items
        self.snackbar.change_style(msg=f"¡Usuario {repr(fullname)} agregado!", style=SnackbarStyle.SUCCESS)
        self.snackbar.update()
        self.update_content()
        self.update_dropdown()

    def add_new_site(self, _: ft.ControlEvent) -> None:
        self.site_dropdown.error_text = None
        self.site_dropdown.update()
        self.s_address.reset_error()
        self.s_username.reset_error()
        self.s_password.reset_error()

        user_email = self.site_dropdown.value
        name = self.s_name.value.strip().capitalize() if self.s_name.value else "Nueva dirección web"
        address = self.rename_address(self.s_address.value.strip())
        username = self.s_username.value.strip()
        password = self.s_password.value.strip()

        # Validate fields
        if not user_email:
            self.site_dropdown.error_text = "¡Debes asociar un usuario al elemento!"
            self.site_dropdown.update()
            return
        if not Validate.is_valid_address(address):
            self.s_address.show_error(msg="¡No es una dirección válida!")
            return
        if not username:
            self.s_username.show_error(msg="¡Se necesita un nombre de usuario!")
            return
        if not password:
            self.s_password.show_error(msg="¡Se necesita una contraseña!")
            return

        self.site_dropdown.error_text = None
        self.site_dropdown.update()
        self.s_address.reset_error()
        self.s_username.reset_error()
        self.s_password.reset_error()

        # New site instance
        user_associate = session.query(User).filter_by(email=user_email).first()
        site = Site(address, username, password, user_associate, name)
        session.add(site)
        session.commit()

        # Reset fields
        self.site_dropdown.value = None
        self.s_name.value = ""
        self.s_address.value = ""
        self.s_username.value = ""
        self.s_password.value = ""
        self.site_form.update()

        # Show & update items
        self.snackbar.change_style(msg=f"¡{repr(name)} agregado con éxito!", style=SnackbarStyle.SUCCESS)
        self.snackbar.update()
        self.update_content()
        self.update_dropdown()

    def add_new_creditcard(self, _: ft.ControlEvent) -> None:
        self.creditcard_dropdown.error_text = None
        self.creditcard_dropdown.update()
        self.cc_number.reset_error()
        self.cc_date.reset_error()
        self.cc_cvc.reset_error()

        user_email = self.creditcard_dropdown.value
        alias = self.cc_alias.value.strip().capitalize() if self.cc_alias.value else "Alias tarjeta"
        cardholder = self.cc_holder.value.strip().title() if self.cc_holder.value else None
        number = self.cc_number.value.strip()
        date = self.cc_date.value.strip()
        cvc = self.cc_cvc.value.strip()

        # Validate fields
        if not user_email:
            self.creditcard_dropdown.error_text = "¡Debes asociar un usuario al elemento!"
            self.creditcard_dropdown.update()
            return
        if not Validate.is_valid_creditcard_number(number):
            self.cc_number.show_error(msg="¡Introduce un número válido de tarjeta!")
            return
        if not Validate.is_valid_date(date):
            self.cc_date.show_error(msg="¡Se necesita una fecha válida!")
            return
        if not cvc:
            self.cc_cvc.show_error(msg="¡CVC necesario!")
            return

        self.creditcard_dropdown.error_text = None
        self.creditcard_dropdown.update()
        self.cc_number.reset_error()
        self.cc_date.reset_error()
        self.cc_cvc.reset_error()

        # New creditcard instance
        user_associate = session.query(User).filter_by(email=user_email).first()
        if cardholder is None:
            cardholder = user_associate.fullname
        date = datetime.strptime(date, "%m/%y")
        creditcard = CreditCard(cardholder, number, cvc, date, user_associate, alias)
        session.add(creditcard)
        session.commit()

        # Reset fields
        self.creditcard_dropdown.value = None
        self.cc_alias.value = ""
        self.cc_holder.value = ""
        self.cc_number.value = ""
        self.cc_date.value = ""
        self.cc_cvc.value = ""
        self.creditcard_form.update()

        # Show & update items
        self.snackbar.change_style(msg=f"¡{repr(alias)} agregada con éxito!", style=SnackbarStyle.SUCCESS)
        self.snackbar.update()
        self.update_content()
        self.update_dropdown()

    def add_new_note(self, _: ft.ControlEvent) -> None:
        self.note_dropdown.error_text = None
        self.note_dropdown.update()
        self.n_content.reset_error()

        user_email = self.note_dropdown.value
        title = self.n_title.value.capitalize().strip() if self.n_title.value else "Nueva nota"
        content = self.n_content.value.strip()

        # Validate fields
        if not user_email:
            self.note_dropdown.error_text = "¡Debes asociar un usuario al elemento!"
            self.note_dropdown.update()
            return
        if not content:
            self.n_content.show_error("¡El campo no puede ir vacío!")
            return

        self.note_dropdown.error_text = None
        self.note_dropdown.update()
        self.n_content.reset_error()

        # New note instance
        user_associate = session.query(User).filter_by(email=user_email).first()
        note = Note(content, user_associate, title)
        session.add(note)
        session.commit()

        # Reset fields
        self.note_dropdown.value = None
        self.n_title.value = ""
        self.n_content.value = ""
        self.note_form.update()

        # Show & update items
        self.snackbar.change_style(msg=f"¡{repr(title)} agregada con éxito!", style=SnackbarStyle.SUCCESS)
        self.snackbar.update()
        self.update_content()
        self.update_dropdown()

    def __populate_rows(self, users: List[User], sites: List[Site], creditcards: List[CreditCard],
                        notes: List[Note], pass_requests: List[PasswordRequest]) -> None:
        self.__clear_rows()
        for user in users:
            self.user_rows.controls.append(
                AdminRow(self.page, user, RowStyle.USER, self.update_content, self.update_dropdown))
        for site in sites:
            self.site_rows.controls.append(
                AdminRow(self.page, site, RowStyle.SITE, self.update_content, self.update_dropdown))
        for creditcard in creditcards:
            self.creditcard_rows.controls.append(
                AdminRow(self.page, creditcard, RowStyle.CREDITCARD, self.update_content, self.update_dropdown))
        for note in notes:
            self.note_rows.controls.append(
                AdminRow(self.page, note, RowStyle.NOTE, self.update_content, self.update_dropdown))
        for request in pass_requests:
            self.pass_request_rows.controls.append(
                AdminRow(self.page, request, RowStyle.PASS_REQUEST, self.update_content, self.update_dropdown))

    def __clear_rows(self) -> None:
        self.user_rows.controls.clear()
        self.site_rows.controls.clear()
        self.creditcard_rows.controls.clear()
        self.note_rows.controls.clear()
        self.pass_request_rows.controls.clear()

    def update_dropdown(self) -> None:
        self.all_users.update()
        self.all_sites.update()
        self.all_creditcards.update()
        self.all_notes.update()
        self.all_requests.update()
        self.site_dropdown.update()
        self.creditcard_dropdown.update()
        self.note_dropdown.update()

    def update_content(self) -> None:
        self.users = session.query(User).all()
        self.sites = session.query(Site).all()
        self.creditcards = session.query(CreditCard).all()
        self.notes = session.query(Note).all()
        self.pass_requests = session.query(PasswordRequest).all()

        self.__populate_rows(self.users, self.sites, self.creditcards, self.notes, self.pass_requests)
        self.site_dropdown.options = [ft.dropdown.Option(user.email) for user in self.users]
        self.creditcard_dropdown.options = [ft.dropdown.Option(user.email) for user in self.users]
        self.note_dropdown.options = [ft.dropdown.Option(user.email) for user in self.users]

    @staticmethod
    def rename_address(new_address: str) -> str:
        address = ""
        if not new_address.startswith(("http://", "https://")):
            address = "http://"
        address += new_address
        if not new_address.endswith("/"):
            address += "/"
        return address
