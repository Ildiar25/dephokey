import flet as ft

from data.db_orm import session

from features.models.user import User
from features.models import Site, CreditCard, Note

from interface.controls import CustomElevatedButton
from interface.pages.forms import GenerateFormStyle, GenerateForm
from interface.pages.body_content import BodyContent
from interface.pages.widgets import *

from shared.utils.colors import *


class CustomSidebar(ft.NavigationRail):
    def __init__(self, page: ft.Page, content: BodyContent) -> None:
        super().__init__()

        # General attributes
        self.page = page
        self.user: User = self.page.session.get("session")
        self.body_content = content

        # Navigation attributes
        self.go_home = ft.NavigationRailDestination(
            ft.Icon(ft.Icons.HOME_ROUNDED, color=selectSidebarColor),
            selected_icon=ft.Icon(ft.Icons.HOME_ROUNDED, color=iconSidebarColor),
            padding=5,
            label_content=ft.Container(
                padding=10,
                content=ft.Text(
                    "Home",
                    font_family="AlbertSansL",
                    color=textSidebarColor
                )
            )
        )
        self.go_sites = ft.NavigationRailDestination(
            ft.Icon(ft.Icons.LANGUAGE_ROUNDED, color=selectSidebarColor),
            selected_icon=ft.Icon(ft.Icons.LANGUAGE_ROUNDED, color=iconSidebarColor),
            padding=5,
            label_content=ft.Container(
                padding=10,
                content=ft.Text(
                    "Sitios Web",
                    font_family="AlbertSansL",
                    color=textSidebarColor
                )
            )
        )
        self.go_cards = ft.NavigationRailDestination(
            ft.Icon(ft.Icons.CREDIT_CARD_ROUNDED, color=selectSidebarColor),
            selected_icon=ft.Icon(ft.Icons.CREDIT_CARD_ROUNDED, color=iconSidebarColor),
            padding=5,
            label_content=ft.Container(
                padding=10,
                content=ft.Text(
                    "Tarjetas",
                    font_family="AlbertSansL",
                    color=textSidebarColor
                )
            )
        )
        self.go_notes = ft.NavigationRailDestination(
            ft.Icon(ft.Icons.NOTES_ROUNDED, color=selectSidebarColor),
            selected_icon=ft.Icon(ft.Icons.NOTES_ROUNDED, color=iconSidebarColor),
            padding=5,
            label_content=ft.Container(
                padding=10,
                content=ft.Text(
                    "Notas",
                    font_family="AlbertSansL",
                    color=textSidebarColor
                )
            )
        )
        self.go_info = ft.NavigationRailDestination(
            ft.Icon(ft.Icons.INFO_ROUNDED, color=selectSidebarColor),
            selected_icon=ft.Icon(ft.Icons.INFO_ROUNDED, color=iconSidebarColor),
            padding=5,
            label_content=ft.Container(
                padding=10,
                content=ft.Text(
                    "Acerca de",
                    font_family="AlbertSansL",
                    color=textSidebarColor
                )
            )
        )

        # Main settings
        self.width = 200
        # self.height = 500
        self.extended = True
        self.visible = True
        self.on_change = self.select_destination

        # Sidebar design
        self.bgcolor = bgSidebarColor
        self.indicator_color = selectSidebarColor
        self.indicator_shape = ft.RoundedRectangleBorder(2)
        self.expand = True

        # Destinations
        self.destinations = [
            self.go_home,
            self.go_sites,
            self.go_cards,
            self.go_notes,
            self.go_info
        ]

    def show_home(self) -> None:
        self.body_content.controls[0].controls[0].value = "Inicio"
        self.body_content.controls[0].controls[1].controls = []
        self.body_content.controls[1].controls = []
        self.body_content.update()

    def show_sites(self) -> None:
        site_buttons = [
            CustomElevatedButton(name="Generar Contraseña", width=187, icon=ft.Icons.PASSWORD_ROUNDED,
                                 foreground_color=accentTextColor, bg_color=neutral05, border_size=1,
                                 on_click=self.open_newpassword_form),
            CustomElevatedButton(name="Nueva Dirección Web", width=197, icon=ft.Icons.ADD_ROUNDED,
                                 foreground_color=tertiaryTextColor, bg_color=primaryCorporateColor,  border_size=-1)
        ]

        self.body_content.controls[0].controls[0].value = "Direcciones web"
        self.body_content.controls[0].controls[1].controls = site_buttons
        self.body_content.controls[1].controls = [SiteWidget(site, self.page) for site in self.user.sites]
        self.body_content.update()

    def show_cards(self) -> None:
        creditcard_buttons = [
            CustomElevatedButton(name="Generar Número", width=187, icon=ft.Icons.ADD_CARD_ROUNDED,
                                 foreground_color=accentTextColor, bg_color=neutral05,border_size=1,
                                 on_click=self.open_newnumber_form),
            CustomElevatedButton(name="Nueva Tarjeta", width=197, icon=ft.Icons.ADD_ROUNDED,
                                 foreground_color=tertiaryTextColor, bg_color=primaryCorporateColor, border_size=-1)
        ]
        self.body_content.controls[0].controls[0].value = "Tarjetas de crédito"
        self.body_content.controls[0].controls[1].controls = creditcard_buttons
        self.body_content.controls[1].controls = []
        self.body_content.update()

    def show_notes(self) -> None:
        note_buttons = [
            CustomElevatedButton(name="Nueva Nota", width=197, icon=ft.Icons.ADD_ROUNDED,
                                 foreground_color=tertiaryTextColor, bg_color=primaryCorporateColor, border_size=-1)
        ]
        self.body_content.controls[0].controls[0].value = "Notas seguras"
        self.body_content.controls[0].controls[1].controls = note_buttons
        self.body_content.controls[1].controls = [NoteWidget(note, self.page) for note in self.user.notes]
        self.body_content.update()

    def show_info(self) -> None:
        self.body_content.controls[0].controls[0].value = "Acerca de"
        self.body_content.controls[0].controls[1].controls = []
        self.body_content.controls[1].controls = []
        self.body_content.update()

    def open_newnumber_form(self, _: ft.ControlEvent) -> None:
        self.page.open(
            GenerateForm(self.page, title="Generar número", generate_style=GenerateFormStyle.NUMBER)
        )

    def open_newpassword_form(self, _: ft.ControlEvent) -> None:
        self.page.open(
            GenerateForm(self.page, title="Generar contraseña", generate_style=GenerateFormStyle.PASSWORD)
        )

    def select_destination(self, event: ft.ControlEvent) -> None:
        match event.control.selected_index:
            case 0:
                self.show_home()

            case 1:
                self.show_sites()

            case 2:
                self.show_cards()

            case 3:
                self.show_notes()

            case 4:
                self.show_info()

            case _:
                pass
