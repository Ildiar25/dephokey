import time
import flet as ft
from typing import List
from sqlalchemy.orm import InstanceState
from datetime import datetime, date, timedelta

from data.db_orm import session

from features.models.user import UserRole, User
from features.models import *

from interface.controls import *

from shared.validate import Validate
from shared.utils.colors import *


class Admin(ft.Column):
    def __init__(self, page: ft.Page) -> None:
        super().__init__()

        # General attributes
        self.page = page
        self.snackbar = ft.SnackBar(
            bgcolor=bgSnackBarDanger,
            content=ft.Text(
                "",
                text_align=ft.TextAlign.CENTER,
                color=mainDangerTextColor
            )
        )
        self.users: List[User] = session.query(User).all()
        self.creditcards: List[CreditCard] = session.query(CreditCard).all()
        self.notes: List[Note] = session.query(Note).all()
        self.sites: List[Site] = session.query(Site).all()
        self.user_selector = ft.Dropdown(
            hint_text="Seleccione usuario",
            border_color=ft.Colors.PURPLE_900,
            options=[
                ft.dropdown.Option(user.email) for user in self.users
            ]
        )

        # Header attributes
        self.name = ft.Text(
            "Ejemplo",  # f"Bienvenido {self.page.session.get('session').fullname}",
            color=lightColorBackground
        )
        self.search_bar = CustomSearchBar(500, self.filter_rows)
        self.logout_button = ft.IconButton(ft.Icons.LOGOUT_ROUNDED,
                                           icon_color=lightColorBackground,
                                           on_click=self.logout)

        # Header content
        self.header = ft.Container(
            height=60,
            bgcolor=ft.Colors.PURPLE_900,
            border_radius=ft.border_radius.only(top_left=5, top_right=5),
            padding=ft.padding.only(left=15, right=15),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[self.name, self.search_bar, self.logout_button]
            )
        )

        # Body attributes
        self.add_user_title = ft.Text(
            "Añadir Usuario:",
            style=ft.TextStyle(font_family="AlbertSansB", size=20)
        )
        self.add_creditcard_title = ft.Text(
            "Añadir Tarjeta de Crédito:",
            style=ft.TextStyle(font_family="AlbertSansB", size=20)
        )
        self.add_note_title = ft.Text(
            "Añadir Nota:",
            style=ft.TextStyle(font_family="AlbertSansB", size=20)
        )
        self.add_site_title = ft.Text(
            "Añadir Sitio:",
            style=ft.TextStyle(font_family="AlbertSansB", size=20)
        )

        # Add user attributes
        self.checkbox_input = CustomCheckbox("ADMINISTRADOR")
        self.user_fullname_input = CustomTextField(label="Nombre Completo", expand=True)
        self.user_email_input = CustomTextField(label="Correo Electrónico", expand=True)
        self.user_password_input = CustomTextField(label="Contraseña", can_reveal_password=True,
                                                   password=True, expand=True)

        # Add user form
        self.add_user_form = ft.Container(
            border_radius=8,
            border=ft.border.all(1, shadowLogForm),
            bgcolor=lightColorBackground,
            padding=15,
            content=ft.Column(
                expand=True,
                controls=[
                    ft.Row(controls=[self.user_fullname_input]),
                    ft.Row(controls=[self.checkbox_input, self.user_email_input, self.user_password_input]),
                    ft.Row(controls=[CustomElevatedButton("AÑADIR USUARIO", width=200,
                                                          on_click=self.add_new_user)],
                           alignment=ft.MainAxisAlignment.END)
                ]
            )
        )

        # Show users data

        # Add creditcard attributes
        self.cardholder_input = CustomTextField(label="Propietario", expand=True)
        self.creditcard_number_input = CustomTextField(label="Número de tarjeta",
                                                       expand=True)
        self.cvc_input = CustomTextField(label="CVC", width=80, input_filter=ft.NumbersOnlyInputFilter())
        self.date_input = ft.IconButton(
            ft.Icons.CALENDAR_MONTH_ROUNDED,
            on_click=lambda _: self.page.open(
                ft.DatePicker(
                    # date_picker_entry_mode=ft.DatePickerEntryMode.INPUT_ONLY,
                    date_picker_mode=ft.DatePickerMode.YEAR,
                    first_date=date.today(),
                    last_date=date.today() + timedelta(days=3652)
                )
            )
        )


        # Add credditcard form
        self.add_creditcard_form = ft.Container(
            border_radius=8,
            border=ft.border.all(1, shadowLogForm),
            bgcolor=lightColorBackground,
            padding=15,
            content=ft.Column(
                expand=True,
                controls=[
                    ft.Row(controls=[self.user_selector, self.cardholder_input]),
                    ft.Row(controls=[self.creditcard_number_input, self.cvc_input, self.date_input]),
                    ft.Row(controls=[CustomElevatedButton("AÑADIR TARJETA", width=200,
                                                          on_click=self.add_new_creditcard)],
                           alignment=ft.MainAxisAlignment.END)
                ]
            )
        )
        # Show creditcards data

        # Add note attribues

        # Add note form

        # Show notes data

        # Add site attributes

        # Add site form

        # Show sites data

        # Page design
        self.expand = True
        self.page.bgcolor = ft.Colors.WHITE
        self.scroll = ft.ScrollMode.HIDDEN

        # Body content
        self.controls = [
            self.header,
            ft.Divider(height=2, color=transparentColor),
            self.add_user_title,
            self.add_user_form,
            ft.Column(
                height=500,
                scroll=ft.ScrollMode.HIDDEN,
                expand=True,
                controls=[
                    ft.Row(
                        controls=[
                            # USER DATA
                        ]
                    )
                ]
            ),
            self.add_creditcard_title,
            self.add_creditcard_form,
            ft.Column(
                height=500,
                scroll=ft.ScrollMode.HIDDEN,
                expand=True,
                controls=[
                    ft.Row(
                        controls=[
                            # CREDITCARD DATA
                        ]
                    )
                ]
            ),
            self.add_note_title,
            ft.Column(
                height=500,
                scroll=ft.ScrollMode.HIDDEN,
                expand=True,
                controls=[
                    ft.Row(
                        controls=[
                            # NOTE DATA
                        ]
                    )
                ]
            ),
            self.add_site_title,
            ft.Column(
                height=500,
                scroll=ft.ScrollMode.HIDDEN,
                expand=True,
                controls=[
                    ft.Row(
                        controls=[
                            # SITE DATA
                        ]
                    )
                ]
            ),
            self.snackbar
        ]

    @staticmethod
    def filter_rows(event) -> None:
        print(f"Filtering information -> {event.data}")

    @staticmethod
    def get_items(object_list: List[User | CreditCard | Note | Site]) -> dict:
        data_dict = {}

        for number_row, data_object in enumerate(object_list):
            row = {}
            for attribute, data in data_object.__dict__.items():
                if isinstance(data, datetime):
                    row[attribute] = data.strftime("%d/%m/%Y %H:%M:%S")
                elif isinstance(data, UserRole):
                    row[attribute] = data.name.upper()
                elif isinstance(attribute, date):
                    row[attribute] = data.strftime("%d/%m/%Y")
                elif not isinstance(data, InstanceState):
                    row[attribute] = data
            data_dict[number_row] = row

        return data_dict

    def logout(self, _: ft.ControlEvent) -> None:
        # Close session
        self.page.session.clear()
        self.page.update()

        # Report page loading
        self.page.overlay.append(
            ft.Container(
                alignment=ft.alignment.center,
                expand=True,
                bgcolor=ft.Colors.with_opacity(0.3, lightColorBackground),
                content=ft.ProgressRing(
                    color=accentGeneralElementColor
                )
            )
        )
        self.page.update()

        # Load login page
        time.sleep(1)
        self.page.overlay.clear()
        self.page.go("/login")

    def add_new_user(self, _: ft.ControlEvent) -> None:

        # Get user inputs
        role: UserRole = UserRole.ADMIN if self.checkbox_input.value else UserRole.CLIENT
        fullname: str = self.user_fullname_input.value.strip()
        username: str = self.user_email_input.value.lower().strip()
        password: str = self.user_password_input.value.strip()

        # Validate all fields
        if not all((self.user_fullname_input.value, self.user_email_input.value, self.user_password_input.value)):
            self.snackbar.content.value = "¡Todos los campos en ## AÑADIR USUARIO ## son obligatorios!"
            self.snackbar.open = True
            self.snackbar.update()

        else:
            # Create new User instance
            new_user: User = User(fullname, username, password, role)

            # Add new user to database
            session.add(new_user)
            session.commit()

            # Reset fields
            self.checkbox_input.value = False
            self.user_fullname_input.value = ""
            self.user_email_input.value = ""
            self.user_password_input.value = ""

            # User info
            self.snackbar.content.value = f"¡Usuario {username} agregado a la base de datos correctamente!"
            self.snackbar.content.color = mainInfoTextColor
            self.snackbar.bgcolor = bgSnackBarInfo
            self.snackbar.open = True
            self.snackbar.update()
            self.page.update()

    def add_new_creditcard(self, _: ft.ControlEvent) -> None:

        # get user inputs
        main_user_input: str = self.user_selector.value
        cardholder_input: str = self.cardholder_input.value
        creditcard_number_input: str = self.creditcard_number_input.value

        if Validate.is_valid_creditcard_number(creditcard_number_input):
            pass

