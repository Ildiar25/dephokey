from collections.abc import Callable
from datetime import datetime

import flet as ft

from data.db_orm import session
from features.models import CreditCard, Note, PasswordRequest, Site
from features.models.user import User, UserRole
from interface.controls import CustomElevatedButton, CustomSwitch, CustomTextField
from interface.controls.e_button import ButtonStyle
from interface.controls.snackbar import Snackbar, SnackbarStyle
from interface.pages.widgets import AdminRow
from interface.pages.widgets.admin_row import RowStyle
from shared.utils.colors import (
    accentTextColor,
    dangerTextColor,
    neutral00,
    neutral20,
    neutral80,
    primaryCorporateColor,
    primaryTextColor,
    secondaryTextColor,
)
from shared.validate import Validate


class AdminPage(ft.Column):
    """Displays admin permissions and allows to modify every database element."""
    def __init__(self, page: ft.Page, snackbar: Snackbar, update_changes: Callable[[], None]) -> None:
        super().__init__()

        # General attributes
        self.page = page
        self.snackbar = snackbar
        self.update_changes = update_changes

        # Admin attributes
        self.users: list[User] = []
        self.sites: list[Site] = []
        self.creditcards: list[CreditCard] = []
        self.notes: list[Note] = []
        self.pass_requests: list[PasswordRequest] = []
        self.span = ft.TextSpan(text="*", style=ft.TextStyle(font_family="AlbertSansB", color=dangerTextColor))
        self.site_dropdown = ft.Dropdown(
            label="Selecciona un correo",
            expand=True,
            label_style=ft.TextStyle(color=secondaryTextColor),
            select_icon=ft.Icons.KEYBOARD_ARROW_DOWN_ROUNDED,
            icon_enabled_color=primaryCorporateColor,
            bgcolor=neutral00,
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
            bgcolor=neutral00,
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
            bgcolor=neutral00,
            border_color=neutral20,
            focused_border_color=primaryCorporateColor,
            border_radius=4,
        )

        # User form fields
        self.u_fullname = CustomTextField(
            hint_text="Introduce el nombre completo del usuario",
            max_length=150
        )
        self.u_email = CustomTextField(
            hint_text="Añade su dirección de correo",
            max_length=50
        )
        self.u_password = CustomTextField(
            hint_text="Incluye una contraseña segura",
            max_length=50,
            password=True,
            can_reveal_password=True
        )
        self.u_switch = CustomSwitch(title="Rol de usuario: ADMIN")
        self.u_submit = CustomElevatedButton(
            name="Añadir usuario",
            style=ButtonStyle.ICON,
            on_click=self.__add_new_user
        )

        # Site form fields
        self.s_name = CustomTextField(
            hint_text="Dale un nombre a la dirección",
            max_length=30
        )
        self.s_address = CustomTextField(
            hint_text="Escribe la dirección",
            max_length=50,
            prefix_text="http://"
        )
        self.s_username = CustomTextField(
            hint_text="Añade el usuario con el que te has registrado",
            max_length=30
        )
        self.s_password = CustomTextField(
            hint_text="Escribe la contraseña",
            max_length=30,
            password=True,
            can_reveal_password=True
        )
        self.s_submit = CustomElevatedButton(
            name="Añadir sitio",
            style=ButtonStyle.ICON,
            on_click=self.__add_new_site
        )

        # Creditcard form fields
        self.cc_alias = CustomTextField(
            hint_text="Agrega un alias",
            max_length=30
        )
        self.cc_holder = CustomTextField(
            hint_text="Introduce el nombre del titular",
            max_length=30
        )
        self.cc_number = CustomTextField(
            hint_text="Añade el número de tarjeta",
            can_reveal_password=True,
            max_length=19,
            password=True,
            input_filter=ft.NumbersOnlyInputFilter()
        )
        self.cc_cvc = CustomTextField(
            hint_text="cvc",
            width=104,
            password=True,
            can_reveal_password=True,
            max_length=4,
            input_filter=ft.NumbersOnlyInputFilter()
        )
        self.cc_date = CustomTextField(
            hint_text="mm/yy",
            max_length=5
        )
        self.cc_submit = CustomElevatedButton(
            name="Añadir tarjeta",
            style=ButtonStyle.ICON,
            on_click=self.__add_new_creditcard
        )

        # Note form fields
        self.n_title = CustomTextField(
            hint_text="Añade un título",
            max_length=25
        )
        self.n_content = CustomTextField(
            hint_text="Agrega contenido importante",
            can_reveal_password=True,
            password=True,
            max_lines=5,
            min_lines=5,
            max_length=324
        )
        self.n_submit = CustomElevatedButton(
            name="Añadir nota",
            style=ButtonStyle.ICON,
            on_click=self.__add_new_note
        )

        # Admin Forms
        self.user_form = ft.Container(
            height=632,
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
                        expand=True,
                        spacing=16,
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Text(
                                        value="Añadir usuario",
                                        font_family="AlbertSansR",
                                        size=18,
                                        color=accentTextColor
                                    ),
                                ]
                            ),
                            ft.Column(
                                spacing=8,
                                controls=[
                                    ft.Text(
                                        value="Nombre completo",
                                        font_family="AlbertSansR",
                                        color=primaryTextColor,
                                        spans=[self.span, ]
                                    ),
                                    self.u_fullname,
                                ]
                            ),
                            ft.Column(
                                spacing=8,
                                controls=[
                                    ft.Text(
                                        value="Correo electrónico",
                                        font_family="AlbertSansR",
                                        color=primaryTextColor,
                                        spans=[self.span, ]
                                    ),
                                    self.u_email,
                                ]
                            ),
                            ft.Column(
                                spacing=8,
                                controls=[
                                    ft.Text(
                                        value="Contraseña",
                                        font_family="AlbertSansR",
                                        color=primaryTextColor,
                                        spans=[self.span, ]
                                    ),
                                    self.u_password,
                                ]
                            ),
                            self.u_switch,
                            ft.Column(
                                expand=True
                            ),
                            ft.Row(alignment=ft.MainAxisAlignment.END,
                                controls=[self.u_submit, ]
                            ),
                        ]
                    ),
                ]
            )
        )
        self.site_form = ft.Container(
            height=632,
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
                        expand=True,
                        spacing=16,
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Text(
                                        value="Añadir sitio web",
                                        font_family="AlbertSansR",
                                        size=18,
                                        color=accentTextColor
                                    ),
                                ]
                            ),
                            ft.Column(
                                spacing=8,
                                controls=[
                                    ft.Text(
                                        value="Usuario asociado",
                                        font_family="AlbertSansR",
                                        color=primaryTextColor,
                                        spans=[self.span, ]
                                    ),
                                    self.site_dropdown,
                                ]
                            ),
                            ft.Column(
                                spacing=8,
                                controls=[
                                    ft.Text(
                                        value="Nombre del sitio",
                                        font_family="AlbertSansR",
                                        color=primaryTextColor,
                                    ),
                                    self.s_name,
                                ]
                            ),
                            ft.Column(
                                spacing=8,
                                controls=[
                                    ft.Text(
                                        value="Dirección web",
                                        font_family="AlbertSansR",
                                        color=primaryTextColor,
                                        spans=[self.span, ]
                                    ),
                                    self.s_address,
                                ]
                            ),
                            ft.Column(
                                spacing=8,
                                controls=[
                                    ft.Text(
                                        value="Nombre de usuario",
                                        font_family="AlbertSansR",
                                        color=primaryTextColor,
                                        spans=[self.span, ]
                                    ),
                                    self.s_username,
                                ]
                            ),
                            ft.Column(
                                spacing=8,
                                controls=[
                                    ft.Text(
                                        value="Contraseña",
                                        font_family="AlbertSansR",
                                        color=primaryTextColor,
                                        spans=[self.span, ]
                                    ),
                                    self.s_password,
                                ]
                            ),
                            ft.Column(
                                expand=True
                            ),
                            ft.Row(
                                alignment=ft.MainAxisAlignment.END,
                                controls=[self.s_submit, ]
                            ),
                        ]
                    ),
                ]
            )
        )
        self.creditcard_form = ft.Container(
            height=632,
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
                        expand=True,
                        spacing=16,
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Text(
                                        value="Añadir tarjeta de crédito",
                                        font_family="AlbertSansR",
                                        size=18,
                                        color=accentTextColor
                                    ),
                                ]
                            ),
                            ft.Column(
                                spacing=8,
                                controls=[
                                    ft.Text(
                                        value="Usuario asociado",
                                        font_family="AlbertSansR",
                                        color=primaryTextColor,
                                        spans=[self.span, ]
                                    ),
                                    self.creditcard_dropdown,
                                ]
                            ),
                            ft.Column(
                                spacing=8,
                                controls=[
                                    ft.Text(
                                        value="Alias",
                                        font_family="AlbertSansR",
                                        color=primaryTextColor
                                    ),
                                    self.cc_alias,
                                ]
                            ),
                            ft.Column(
                                spacing=8,
                                controls=[
                                    ft.Text(
                                        value="Nombre del titular",
                                        font_family="AlbertSansR",
                                        color=primaryTextColor
                                    ),
                                    self.cc_holder,
                                ]
                            ),
                            ft.Column(
                                spacing=8,
                                controls=[
                                    ft.Text(
                                        value="Número de la tarjeta",
                                        font_family="AlbertSansR",
                                        color=primaryTextColor,
                                        spans=[self.span, ]
                                    ),
                                    self.cc_number,
                                ]
                            ),
                            ft.Row(
                                spacing=16,
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Column(
                                        spacing=8,
                                        expand=True,
                                        controls=[
                                            ft.Text(
                                                value="Caducidad",
                                                font_family="AlbertSansR",
                                                color=primaryTextColor,
                                                spans=[self.span, ]
                                            ),
                                            self.cc_date,
                                        ]
                                    ),
                                    ft.VerticalDivider(),
                                    ft.Column(
                                        spacing=8,
                                        controls=[
                                            ft.Text(
                                                value="CVC",
                                                font_family="AlbertSansR",
                                                color=primaryTextColor,
                                                spans=[self.span, ]
                                            ),
                                            self.cc_cvc,
                                        ]
                                    ),
                                ]
                            ),
                            ft.Column(
                                expand=True
                            ),
                            ft.Row(
                                alignment=ft.MainAxisAlignment.END,
                                controls=[self.cc_submit, ]
                            )
                        ]
                    )
                ]
            )
        )
        self.note_form = ft.Container(
            height=632,
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
                        expand=True,
                        spacing=16,
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Text(
                                        value="Añadir nota segura",
                                        font_family="AlbertSansR",
                                        size=18,
                                        color=accentTextColor
                                    ),
                                ]
                            ),
                            ft.Column(
                                spacing=8,
                                controls=[
                                    ft.Text(
                                        value="Usuario asociado",
                                        font_family="AlbertSansR",
                                        color=primaryTextColor,
                                        spans=[self.span, ]
                                    ),
                                    self.note_dropdown,
                                ]
                            ),
                            ft.Column(
                                spacing=8,
                                controls=[
                                    ft.Text(
                                        value="Título de la nota",
                                        font_family="AlbertSansR",
                                        color=primaryTextColor
                                    ),
                                    self.n_title,
                                ]
                            ),
                            ft.Column(
                                spacing=8,
                                controls=[
                                    ft.Text(
                                        value="Contenido",
                                        font_family="AlbertSansR",
                                        color=primaryTextColor,
                                        spans=[self.span, ]
                                    ),
                                    self.n_content,
                                ]
                            ),
                            ft.Column(
                                expand=True
                            ),
                            ft.Row(
                                alignment=ft.MainAxisAlignment.END,
                                controls=[self.n_submit, ]
                            ),
                        ]
                    ),
                ]
            )
        )

        # Item rows
        self.user_rows = ft.Column()
        self.site_rows = ft.Column()
        self.creditcard_rows = ft.Column()
        self.note_rows = ft.Column()
        self.pass_request_rows = ft.Column()

        # Item dropdowns
        self.users_display = ft.Container(
            expand=True,
            bgcolor=neutral00,
            border_radius=4,
            shadow=ft.BoxShadow(
                blur_radius=0.9,
                offset=(0.0, 0.5),
                color=ft.Colors.with_opacity(opacity=0.3, color=neutral80)
            ),
            content=ft.ExpansionTile(
                title=ft.Text(value="Usuarios", size=20, color=accentTextColor),
                controls_padding=ft.padding.all(22),
                shape=ft.RoundedRectangleBorder(4),
                collapsed_shape=ft.RoundedRectangleBorder(4),
                min_tile_height=44,
                bgcolor=neutral00,
                collapsed_bgcolor=neutral00,
                controls=[self.user_rows, ]
            )
        )
        self.sites_display = ft.Container(
            expand=True,
            bgcolor=neutral00,
            border_radius=4,
            shadow=ft.BoxShadow(
                blur_radius=0.9,
                offset=(0.0, 0.5),
                color=ft.Colors.with_opacity(opacity=0.3, color=neutral80)
            ),
            content=ft.ExpansionTile(
                title=ft.Text(value="Sitios web", size=20, color=accentTextColor),
                controls_padding=ft.padding.all(22),
                shape=ft.RoundedRectangleBorder(4),
                collapsed_shape=ft.RoundedRectangleBorder(4),
                min_tile_height=44,
                bgcolor=neutral00,
                collapsed_bgcolor=neutral00,
                controls=[self.site_rows, ]
            )
        )
        self.creditcards_display = ft.Container(
            expand=True,
            bgcolor=neutral00,
            border_radius=4,
            shadow=ft.BoxShadow(
                blur_radius=0.9,
                offset=(0.0, 0.5),
                color=ft.Colors.with_opacity(opacity=0.3, color=neutral80)
            ),
            content=ft.ExpansionTile(
                title=ft.Text(value="Tarjetas de crédito", size=20, color=accentTextColor),
                controls_padding=ft.padding.all(22),
                shape=ft.RoundedRectangleBorder(4),
                collapsed_shape=ft.RoundedRectangleBorder(4),
                min_tile_height=44,
                bgcolor=neutral00,
                collapsed_bgcolor=neutral00,
                controls=[self.creditcard_rows, ]
            )
        )
        self.notes_display = ft.Container(
            expand=True,
            bgcolor=neutral00,
            border_radius=4,
            shadow=ft.BoxShadow(
                blur_radius=0.9,
                offset=(0.0, 0.5),
                color=ft.Colors.with_opacity(opacity=0.3, color=neutral80)
            ),
            content=ft.ExpansionTile(
                title=ft.Text(value="Notas seguras", size=20, color=accentTextColor),
                controls_padding=ft.padding.all(22),
                shape=ft.RoundedRectangleBorder(4),
                collapsed_shape=ft.RoundedRectangleBorder(4),
                min_tile_height=44,
                bgcolor=neutral00,
                collapsed_bgcolor=neutral00,
                controls=[self.note_rows, ]
            )
        )
        self.requests_display = ft.Container(
            expand=True,
            bgcolor=neutral00,
            border_radius=4,
            shadow=ft.BoxShadow(
                blur_radius=0.9,
                offset=(0.0, 0.5),
                color=ft.Colors.with_opacity(opacity=0.3, color=neutral80)
            ),
            content=ft.ExpansionTile(
                title=ft.Text(value="Peticiones de cambio de contraseña", size=20, color=accentTextColor),
                controls_padding=ft.padding.all(22),
                shape=ft.RoundedRectangleBorder(4),
                collapsed_shape=ft.RoundedRectangleBorder(4),
                min_tile_height=44,
                bgcolor=neutral00,
                collapsed_bgcolor=neutral00,
                controls=[self.pass_request_rows, ]
            )
        )

        # Design settings
        self.espacing = 32

        # Page content
        self.controls = [
            ft.Row(
                expand=True,
                spacing=32,
                controls=[
                    # Forms
                    self.user_form,
                    self.creditcard_form,
                    self.site_form,
                    self.note_form,
                ]
            ),
            ft.Divider(
                height=32, thickness=3, color=neutral20
            ),
            ft.Column(
                spacing=32,
                controls=[
                    # Dropdowns
                    self.users_display,
                    self.sites_display,
                    self.creditcards_display,
                    self.notes_display,
                    self.requests_display,
                ]
            ),
        ]

        self.update_content()

    def __add_new_user(self, _: ft.ControlEvent) -> None:
        self.__reset_all_textield_errors()

        fullname = self.u_fullname.value.strip().title()
        email = self.u_email.value.strip().lower()
        password = self.u_password.value.strip()
        role = UserRole.ADMIN if self.u_switch.get_value() else UserRole.CLIENT

        # Validate fields
        if not fullname:
            self.u_fullname.show_error("¡El usuario debe tener un nombre!")
            return

        if session.query(User).filter_by(email=email).first():
            self.u_email.show_error("¡Ese correo ya existe!")
            return

        if not Validate.is_valid_email(email):
            self.u_email.show_error("¡Se necesita un correo electrónico válido!")
            return

        if not Validate.is_valid_password(password):
            self.u_password.show_error("¡La contraseña necesita números, mayúsculas y minúsculas")
            return

        self.__reset_all_textield_errors()

        # New user instance
        user = User(fullname, email, password, role)
        self.__save_data(user)

        # Reset user form
        self.__reset_user_form()

        # Show & update items
        self.update_content()
        self.__display_message(msg=f"¡Usuario {repr(fullname)} agregado!", style=SnackbarStyle.SUCCESS)
        self.__update_display()

    def __add_new_site(self, _: ft.ControlEvent) -> None:
        self.__reset_all_textield_errors()

        user = self.__get_user_intance(self.site_dropdown.value)
        if not user:
            self.dropdown_show_error(msg="¡Debes asociar un usuario al elemento!", dropdown=self.site_dropdown)
            return

        name = self.s_name.value.strip().capitalize() if self.s_name.value else "Nueva dirección web"
        address = self.__rename_address(self.s_address.value.strip())
        username = self.s_username.value.strip()
        password = self.s_password.value.strip()

        # Validate fields
        if not Validate.is_valid_address(address):
            self.s_address.show_error(msg="¡No es una dirección válida!")
            return

        if not username:
            self.s_username.show_error(msg="¡Se necesita un nombre de usuario!")
            return

        if not password:
            self.s_password.show_error(msg="¡Se necesita una contraseña!")
            return

        self.__reset_all_textield_errors()

        # New site instance
        site = Site(address, username, password, user, name)
        self.__save_data(site)

        # Reset site form
        self.__reset_site_form()

        # Show & update items
        self.update_content()
        self.__display_message(msg=f"¡{repr(name)} agregado con éxito!", style=SnackbarStyle.SUCCESS)
        self.__update_display()

    def __add_new_creditcard(self, _: ft.ControlEvent) -> None:
        self.__reset_all_textield_errors()

        user = self.__get_user_intance(self.creditcard_dropdown.value)
        if not user:
            self.dropdown_show_error(msg="¡Debes asociar un usuario al elemento!", dropdown=self.creditcard_dropdown)
            return

        alias = self.cc_alias.value.strip().capitalize() if self.cc_alias.value else "Alias tarjeta"
        cardholder = self.cc_holder.value.strip().title() if self.cc_holder.value else user.fullname
        number = self.cc_number.value.strip()
        date = self.cc_date.value.strip()
        cvc = self.cc_cvc.value.strip()

        # Validate fields
        if not Validate.is_valid_creditcard_number(number):
            self.cc_number.show_error(msg="¡Introduce un número válido de tarjeta!")
            return

        if not Validate.is_valid_date(date):
            self.cc_date.show_error(msg="¡Se necesita una fecha válida!")
            return

        if not cvc:
            self.cc_cvc.show_error(msg="¡CVC necesario!")
            return

        self.__reset_all_textield_errors()
        date = datetime.strptime(date, "%m/%y")

        # New creditcard instance
        creditcard = CreditCard(cardholder, number, cvc, date, user, alias)
        self.__save_data(creditcard)

        # Reset creditcard form
        self.__reset_creditcard_form()

        # Show & update items
        self.update_content()
        self.__display_message(msg=f"¡{repr(alias)} agregada con éxito!", style=SnackbarStyle.SUCCESS)
        self.__update_display()

    def __add_new_note(self, _: ft.ControlEvent) -> None:
        self.__reset_all_textield_errors()

        user = self.__get_user_intance(self.note_dropdown.value)
        if not user:
            self.dropdown_show_error(msg="¡Debes asociar un usuario al elemento!", dropdown=self.note_dropdown)
            return

        title = self.n_title.value.capitalize().strip() if self.n_title.value else "Nueva nota"
        content = self.n_content.value.strip()

        # Validate fields
        if not content:
            self.n_content.show_error("¡El campo no puede ir vacío!")
            return

        self.__reset_all_textield_errors()

        # New note instance
        note = Note(content, user, title)
        self.__save_data(note)

        # Reset note form
        self.__reset_note_form()

        # Show & update items
        self.update_content()
        self.__display_message(msg=f"¡{repr(title)} agregada con éxito!", style=SnackbarStyle.SUCCESS)
        self.__update_display()

    def update_content(self) -> None:
        self.__request_new_data()
        self.__update_dropdown_options()
        self.__populate_rows(self.users, self.sites, self.creditcards, self.notes, self.pass_requests)

    def __reset_all_textield_errors(self) -> None:
        self.cc_cvc.reset_error()
        self.cc_date.reset_error()
        self.cc_number.reset_error()
        self.n_content.reset_error()
        self.s_address.reset_error()
        self.s_password.reset_error()
        self.s_username.reset_error()
        self.u_email.reset_error()
        self.u_fullname.reset_error()
        self.u_password.reset_error()

        self.dropdown_reset_error(self.creditcard_dropdown)
        self.dropdown_reset_error(self.note_dropdown)
        self.dropdown_reset_error(self.site_dropdown)

    def __reset_creditcard_form(self) -> None:
        self.creditcard_dropdown.value = None
        self.cc_alias.value = ""
        self.cc_holder.value = ""
        self.cc_number.value = ""
        self.cc_date.value = ""
        self.cc_cvc.value = ""
        self.creditcard_form.update()

    def __reset_note_form(self) -> None:
        self.note_dropdown.value = None
        self.n_title.value = ""
        self.n_content.value = ""
        self.note_form.update()

    def __reset_site_form(self) -> None:
        self.site_dropdown.value = None
        self.s_name.value = ""
        self.s_address.value = ""
        self.s_username.value = ""
        self.s_password.value = ""
        self.site_form.update()

    def __reset_user_form(self) -> None:
        self.u_fullname.value = ""
        self.u_email.value = ""
        self.u_password.value = ""
        self.u_switch.set_value(False)
        self.user_form.update()

    def __display_message(self, msg: str, style: SnackbarStyle):
        self.snackbar.change_style(msg=msg, style=style)
        self.snackbar.update()

    def __request_new_data(self) -> None:
        self.users = session.query(User).all()
        self.sites = session.query(Site).all()
        self.creditcards = session.query(CreditCard).all()
        self.notes = session.query(Note).all()
        self.pass_requests = session.query(PasswordRequest).all()

    def __update_dropdown_options(self) -> None:
        self.site_dropdown.options = [ft.dropdown.Option(user.email) for user in self.users]
        self.creditcard_dropdown.options = [ft.dropdown.Option(user.email) for user in self.users]
        self.note_dropdown.options = [ft.dropdown.Option(user.email) for user in self.users]

    def __populate_rows(
            self,
            users: list[User],
            sites: list[Site],
            creditcards: list[CreditCard],
            notes: list[Note],
            pw_requests: list[PasswordRequest]
    ) -> None:
        self.__clear_rows()
        self.__append_item(users, RowStyle.USER, self.user_rows.controls)
        self.__append_item(sites, RowStyle.SITE, self.site_rows.controls)
        self.__append_item(creditcards, RowStyle.CREDITCARD, self.creditcard_rows.controls)
        self.__append_item(notes, RowStyle.NOTE, self.note_rows.controls)
        self.__append_item(pw_requests, RowStyle.PASS_REQUEST, self.pass_request_rows.controls)

    def __append_item(
            self, items: list[User | Site | CreditCard | Note | PasswordRequest],
            style: RowStyle,
            target: list
    ) -> None:
        for item in items:
            target.append(
                AdminRow(
                    page=self.page,
                    item=item,
                    style=style,
                    update_appearance=self.update_content,
                    update_dropdown=self.__update_display
                )
            )

    def __clear_rows(self) -> None:
        self.user_rows.controls.clear()
        self.site_rows.controls.clear()
        self.creditcard_rows.controls.clear()
        self.note_rows.controls.clear()
        self.pass_request_rows.controls.clear()

    def __update_display(self) -> None:
        self.update()

    @staticmethod
    def __save_data(item: CreditCard | Note | PasswordRequest | Site | User) -> None:
        session.add(item)
        session.commit()

    @staticmethod
    def __get_user_intance(email: str) -> User:
        return session.query(User).filter_by(email=email).first()

    @staticmethod
    def __rename_address(web_address: str) -> str:
        address = ""
        if not web_address.startswith(("http://", "https://")):
            address = "http://"

        address += web_address
        if not web_address.endswith("/"):
            address += "/"

        return address

    @staticmethod
    def dropdown_show_error(msg: str, dropdown: ft.Dropdown) -> None:
        dropdown.error_text = msg
        dropdown.update()

    @staticmethod
    def dropdown_reset_error(dropdown: ft.Dropdown) -> None:
        dropdown.error_text = None
        dropdown.update()
