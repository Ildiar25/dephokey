import flet as ft

from shared.utils.colors import *


class CustomSidebar(ft.NavigationRail):
    def __init__(self, page: ft.Page, content: ft.Container) -> None:
        super().__init__()

        # General attributes
        self.page = page
        self.active_content = content

        # Navigation attributes
        self.go_home = ft.NavigationRailDestination(
            ft.Icon(ft.Icons.HOME_ROUNDED, color=accentSidebar),
            selected_icon=ft.Icon(ft.Icons.HOME_ROUNDED, color=textColorSidebar),
            padding=5,
            label_content=ft.Container(
                padding=10,
                content=ft.Text(
                    "Home",
                    font_family="AlbertSansL",
                    color=textColorSidebar
                )
            )
        )
        self.go_sites = ft.NavigationRailDestination(
            ft.Icon(ft.Icons.WEBHOOK_ROUNDED, color=accentSidebar),
            selected_icon=ft.Icon(ft.Icons.WEBHOOK_ROUNDED, color=textColorSidebar),
            padding=5,
            label_content=ft.Container(
                padding=10,
                content=ft.Text(
                    "Sitios Web",
                    font_family="AlbertSansL",
                    color=textColorSidebar
                )
            )
        )
        self.go_cards = ft.NavigationRailDestination(
            ft.Icon(ft.Icons.CREDIT_CARD_ROUNDED, color=accentSidebar),
            selected_icon=ft.Icon(ft.Icons.CREDIT_CARD_ROUNDED, color=textColorSidebar),
            padding=5,
            label_content=ft.Container(
                padding=10,
                content=ft.Text(
                    "Tarjetas",
                    font_family="AlbertSansL",
                    color=textColorSidebar
                )
            )
        )
        self.go_notes = ft.NavigationRailDestination(
            ft.Icon(ft.Icons.NOTES_ROUNDED, color=accentSidebar),
            selected_icon=ft.Icon(ft.Icons.NOTES_ROUNDED, color=textColorSidebar),
            padding=5,
            label_content=ft.Container(
                padding=10,
                content=ft.Text(
                    "Notas",
                    font_family="AlbertSansL",
                    color=textColorSidebar
                )
            )
        )
        self.go_info = ft.NavigationRailDestination(
            ft.Icon(ft.Icons.INFO_ROUNDED, color=accentSidebar),
            selected_icon=ft.Icon(ft.Icons.INFO_ROUNDED, color=textColorSidebar),
            padding=5,
            label_content=ft.Container(
                padding=10,
                content=ft.Text(
                    "Acerca de",
                    font_family="AlbertSansL",
                    color=textColorSidebar
                )
            )
        )

        # Main settings
        self.width = 200
        self.height = 5000
        self.extended = True
        self.visible = True
        self.on_change = self.select_destination

        # Sidebar design
        self.bgcolor = bgSidebar
        self.indicator_color = accentSidebar
        self.indicator_shape = ft.RoundedRectangleBorder(2)

        # Destinations
        self.destinations = [
            self.go_home,
            self.go_sites,
            self.go_cards,
            self.go_notes,
            self.go_info
        ]

    def show_home(self):
        self.active_content.content = ft.Text("Muestra HOME")
        self.active_content.update()

    def show_sites(self):
        self.active_content.content = ft.Text("Muestra SITIOS")
        self.active_content.update()

    def show_cards(self):
        self.active_content.content = ft.Text("Muestra TARJETAS")
        self.active_content.update()

    def show_notes(self):
        self.active_content.content = ft.Text("Muestra NOTAS")
        self.active_content.update()

    def show_info(self):
        self.active_content.content = ft.Text("Muestra ACERCA DE")
        self.active_content.update()

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
