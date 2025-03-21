import flet as ft

from features.models.user import User, UserRole
from interface.controls import CustomElevatedButton
from interface.controls.e_button import ButtonStyle
from interface.controls.snackbar import Snackbar
from interface.pages.content_manager import ContentManager, ContentStyle
from interface.pages.forms import CreditCardForm, GenerateForm, NoteForm, SiteForm
from interface.pages.forms.base_form import FormStyle
from shared.logger_setup import main_log as log
from shared.utils.colors import neutral05, neutral80, primaryCorporateColor, tertiaryTextColor


class CustomSidebar(ft.NavigationRail):
    """Creates a navigation rail between given destinations."""
    def __init__(self, page: ft.Page, snackbar: Snackbar, content: ContentManager) -> None:
        super().__init__()

        # General attributes
        self.page = page
        self.snackbar = snackbar
        self.body_content = content

        # Navigation attributes
        self.user: User = self.page.session.get("session")
        self.go_home = ft.NavigationRailDestination(
            icon=ft.Icon(ft.Icons.HOME_ROUNDED, color=primaryCorporateColor),
            selected_icon=ft.Icon(ft.Icons.HOME_ROUNDED, color=neutral05),
            padding=5,
            label_content=ft.Container(
                padding=10,
                content=ft.Text(
                    value="Inicio",
                    font_family="AlbertSansL",
                    color=tertiaryTextColor
                )
            )
        )
        self.go_sites = ft.NavigationRailDestination(
            icon=ft.Icon(ft.Icons.LANGUAGE_ROUNDED, color=primaryCorporateColor),
            selected_icon=ft.Icon(ft.Icons.LANGUAGE_ROUNDED, color=neutral05),
            padding=5,
            label_content=ft.Container(
                padding=10,
                content=ft.Text(
                    value="Sitios Web",
                    font_family="AlbertSansL",
                    color=tertiaryTextColor
                )
            )
        )
        self.go_cards = ft.NavigationRailDestination(
            icon=ft.Icon(ft.Icons.CREDIT_CARD_ROUNDED, color=primaryCorporateColor),
            selected_icon=ft.Icon(ft.Icons.CREDIT_CARD_ROUNDED, color=neutral05),
            padding=5,
            label_content=ft.Container(
                padding=10,
                content=ft.Text(
                    value="Tarjetas",
                    font_family="AlbertSansL",
                    color=tertiaryTextColor
                )
            )
        )
        self.go_notes = ft.NavigationRailDestination(
            icon=ft.Icon(ft.Icons.NOTES_ROUNDED, color=primaryCorporateColor),
            selected_icon=ft.Icon(ft.Icons.NOTES_ROUNDED, color=neutral05),
            padding=5,
            label_content=ft.Container(
                padding=10,
                content=ft.Text(
                    value="Notas",
                    font_family="AlbertSansL",
                    color=tertiaryTextColor
                )
            )
        )
        self.go_info = ft.NavigationRailDestination(
            icon=ft.Icon(ft.Icons.INFO_ROUNDED, color=primaryCorporateColor),
            selected_icon=ft.Icon(ft.Icons.INFO_ROUNDED, color=neutral05),
            padding=5,
            label_content=ft.Container(
                padding=10,
                content=ft.Text(
                    value="Acerca de",
                    font_family="AlbertSansL",
                    color=tertiaryTextColor
                )
            )
        )

        # Main settings
        self.width = 200
        self.extended = True
        self.visible = self.user.role == UserRole.CLIENT
        self.on_change = self.__select_page_target

        # Sidebar design
        self.bgcolor = neutral80
        self.indicator_color = primaryCorporateColor
        self.indicator_shape = ft.RoundedRectangleBorder(4)
        self.expand = True

        # Destinations
        self.destinations = [self.go_home, self.go_sites, self.go_cards, self.go_notes, self.go_info, ]

    def __show_home(self) -> None:
        log.info("Redirigiendo a HOME.")
        self.body_content.change_content(title="¡Bienvenido a Dephokey!", style=ContentStyle.HOME)
        self.body_content.update()

    def __show_sites(self) -> None:
        log.info("Redirigiendo a SITES.")
        site_buttons = [
            CustomElevatedButton(
                name="Generar contraseña",
                style=ButtonStyle.BORDER,
                on_click=self.__open_generate_pw_form,
                icon=ft.Icons.PASSWORD_ROUNDED
            ),
            CustomElevatedButton(
                name="Nueva dirección web",
                style=ButtonStyle.ICON,
                on_click=self.__open_site_form
            ),
        ]

        self.body_content.change_content(title="Direcciones web", style=ContentStyle.SITES, buttons=site_buttons)
        self.body_content.update()

    def __show_creditcards(self) -> None:
        log.info("Redirigiendo a CREDITCARDS.")
        creditcard_buttons = [
            CustomElevatedButton(
                name="Generar número",
                style=ButtonStyle.BORDER,
                on_click=self.__open_generate_cc_form,
                icon=ft.Icons.ADD_CARD_ROUNDED
            ),
            CustomElevatedButton(
                name="Nueva tarjeta de crédito",
                style=ButtonStyle.ICON,
                on_click=self.__open_creditcard_form
            ),
        ]

        self.body_content.change_content(
            title="Tarjetas de crédito", style=ContentStyle.CREDITCARDS, buttons=creditcard_buttons
        )
        self.body_content.update()

    def __show_notes(self) -> None:
        log.info("Redirigiendo a NOTES.")
        note_buttons = [
            CustomElevatedButton(
                name="Nueva nota segura",
                style=ButtonStyle.ICON,
                on_click=self.__open_note_form
            ),
        ]

        self.body_content.change_content(title="Notas seguras", style=ContentStyle.NOTES, buttons=note_buttons)
        self.body_content.update()

    def __show_info(self) -> None:
        log.info("Redirigiendo a ABOUT.")
        self.body_content.change_content(title="Acerca de", style=ContentStyle.ABOUT)
        self.body_content.update()

    def __open_creditcard_form(self, _: ft.ControlEvent) -> None:
        self.page.open(
            CreditCardForm(
                title="Nueva tarjeta de crédito",
                page=self.page,
                snackbar=self.snackbar,
                style=FormStyle.ADD,
                update_changes=self.body_content.confirm_changes
            )
        )

    def __open_note_form(self, _: ft.ControlEvent) -> None:
        self.page.open(
            NoteForm(
                title="Nueva nota segura",
                page=self.page,
                snackbar=self.snackbar,
                style=FormStyle.ADD,
                update_changes=self.body_content.confirm_changes
            )
        )

    def __open_site_form(self, _: ft.ControlEvent) -> None:
        self.page.open(
            SiteForm(
                title="Nueva dirección web",
                page=self.page,
                snackbar=self.snackbar,
                style=FormStyle.ADD,
                update_changes=self.body_content.confirm_changes
            )
        )

    def __open_generate_cc_form(self, _: ft.ControlEvent) -> None:
        self.page.open(
            GenerateForm(title="Generar número", page=self.page, style=FormStyle.GENERATE_CC)
        )

    def __open_generate_pw_form(self, _: ft.ControlEvent) -> None:
        self.page.open(
            GenerateForm(title="Generar contraseña", page=self.page, style=FormStyle.GENERATE_PW)
        )

    def __select_page_target(self, event: ft.ControlEvent) -> None:
        match event.control.selected_index:
            case 0:
                self.__show_home()

            case 1:
                self.__show_sites()

            case 2:
                self.__show_creditcards()

            case 3:
                self.__show_notes()

            case 4:
                self.__show_info()
