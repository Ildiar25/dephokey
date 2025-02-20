import flet as ft

from features.models.user import User, UserRole

from interface.controls import *
from interface.pages.forms import GenerateFormStyle, GenerateForm, AddFormStyle, AddForm
from interface.pages.body_content import BodyContent, ContentStyle

from shared.utils.colors import *


class CustomSidebar(ft.NavigationRail):
    def __init__(self, page: ft.Page, content: BodyContent) -> None:
        super().__init__()

        # General attributes
        self.page = page
        self.body_content = content

        # Navigation attributes
        self.user: User = self.page.session.get("session")
        self.go_home = ft.NavigationRailDestination(
            ft.Icon(ft.Icons.HOME_ROUNDED, color=selectSidebarColor),
            selected_icon=ft.Icon(ft.Icons.HOME_ROUNDED, color=iconSidebarColor),
            padding=5,
            label_content=ft.Container(
                padding=10,
                content=ft.Text(
                    "Inicio",
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
        self.extended = True
        self.visible = True if self.user.role == UserRole.CLIENT else False
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
        self.body_content.change_content(title="Inicio", style=ContentStyle.HOME)
        self.body_content.update()

    def show_sites(self) -> None:
        site_buttons = [
            CustomElevatedButton(
                name="Generar contraseña", style=ButtonStyle.BORDER, on_click=self.open_newpassword_form,
                icon=ft.Icons.PASSWORD_ROUNDED),
            CustomElevatedButton(
                name="Nueva dirección web", style=ButtonStyle.ICON, on_click=self.add_newsite_form)
        ]

        self.body_content.change_content(
            title="Direcciones web", style=ContentStyle.SITES, buttons=site_buttons
        )
        self.body_content.update()

    def show_cards(self) -> None:
        creditcard_buttons = [
            CustomElevatedButton(
                name="Generar número", style=ButtonStyle.BORDER, on_click=self.open_newnumber_form,
                icon=ft.Icons.ADD_CARD_ROUNDED),
            CustomElevatedButton(
                name="Nueva tarjeta de crédito", style=ButtonStyle.ICON, on_click=self.add_newcreditcard_form)
        ]
        self.body_content.change_content(
            title="Tarjetas de crédito", style=ContentStyle.CREDITCARDS, buttons=creditcard_buttons
        )
        self.body_content.update()

    def show_notes(self) -> None:
        note_buttons = [
            CustomElevatedButton(
                name="Nueva nota segura", style=ButtonStyle.ICON, on_click=self.add_newnote_form)
        ]
        self.body_content.change_content(title="Notas seguras", style=ContentStyle.NOTES, buttons=note_buttons)
        self.body_content.update()

    def show_info(self) -> None:
        self.body_content.change_content(title="Acerca de", style=ContentStyle.ABOUT)
        self.body_content.update()

    def add_newsite_form(self, _: ft.ControlEvent) -> None:
        self.page.open(
            AddForm(self.page, title="Nueva Dirección Web", addform_style=AddFormStyle.SITE)
        )

    def add_newcreditcard_form(self, _: ft.ControlEvent) -> None:
        self.page.open(
            AddForm(self.page, title="Nueva Tarjeta de Crédito", addform_style=AddFormStyle.CREDITCARD)
        )

    def add_newnote_form(self, _: ft.ControlEvent) -> None:
        self.page.open(
            AddForm(self.page, title="Nueva Nota Segura", addform_style=AddFormStyle.NOTE)
        )


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
