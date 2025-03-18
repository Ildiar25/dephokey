import flet as ft

from features.models.user import User, UserRole

from interface.controls import *
from interface.pages.forms import FormStyle, SiteForm, CreditCardForm, NoteForm, GenerateForm
from interface.pages.content_manager import BodyContent, ContentStyle

from shared.logger_setup import main_log as log
from shared.utils.colors import *


class CustomSidebar(ft.NavigationRail):
    def __init__(self, page: ft.Page, snackbar: Snackbar, content: BodyContent) -> None:
        super().__init__()

        # General attributes
        self.page = page
        self.snackbar = snackbar
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
        self.indicator_shape = ft.RoundedRectangleBorder(4)
        self.expand = True

        # Destinations
        self.destinations = [self.go_home, self.go_sites, self.go_cards, self.go_notes, self.go_info]

    def show_home(self) -> None:
        log.info("Redirigiendo a HOME.")
        self.body_content.change_content(title="¡Bienvenido a Dephokey!", style=ContentStyle.HOME)
        self.body_content.update()

    def show_sites(self) -> None:
        log.info("Redirigiendo a SITES.")
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

    def show_creditcards(self) -> None:
        log.info("Redirigiendo a CREDITCARDS.")
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
        log.info("Redirigiendo a NOTES.")
        note_buttons = [
            CustomElevatedButton(
                name="Nueva nota segura", style=ButtonStyle.ICON, on_click=self.add_newnote_form)
        ]
        self.body_content.change_content(title="Notas seguras", style=ContentStyle.NOTES, buttons=note_buttons)
        self.body_content.update()

    def show_info(self) -> None:
        log.info("Redirigiendo a ABOUT.")
        self.body_content.change_content(title="Acerca de", style=ContentStyle.ABOUT)
        self.body_content.update()

    def add_newsite_form(self, _: ft.ControlEvent) -> None:
        self.page.open(
            SiteForm(
                title="Nueva dirección web", page=self.page, snackbar=self.snackbar, style=FormStyle.ADD,
                update_changes=self.body_content.update_changes
            )
        )

    def add_newcreditcard_form(self, _: ft.ControlEvent) -> None:
        self.page.open(
            CreditCardForm(
                title="Nueva tarjeta de crédito", page=self.page, snackbar=self.snackbar, style=FormStyle.ADD,
                update_changes=self.body_content.update_changes
            )
        )

    def add_newnote_form(self, _: ft.ControlEvent) -> None:
        self.page.open(
            NoteForm(
                title="Nueva nota segura", page=self.page, snackbar=self.snackbar, style=FormStyle.ADD,
                update_changes=self.body_content.update_changes
            )
        )

    def open_newnumber_form(self, _: ft.ControlEvent) -> None:
        self.page.open(
            GenerateForm(title="Generar número", page=self.page, style=FormStyle.CC_NUMBER)
        )

    def open_newpassword_form(self, _: ft.ControlEvent) -> None:
        self.page.open(
            GenerateForm(title="Generar contraseña", page=self.page, style=FormStyle.PASSWORD)
        )

    def select_destination(self, event: ft.ControlEvent) -> None:
        match event.control.selected_index:
            case 0:
                self.show_home()

            case 1:
                self.show_sites()

            case 2:
                self.show_creditcards()

            case 3:
                self.show_notes()

            case 4:
                self.show_info()
