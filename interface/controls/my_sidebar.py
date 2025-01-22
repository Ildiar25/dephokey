import flet as ft


class CustomSidebar(ft.NavigationRail):

    def __init__(self) -> None:
        super().__init__()

        # General settings
        self.visible = True

        self.extended = True
        self.width = 200
        self.height = 2000


        self.destinations = [
            ft.NavigationRailDestination(
                icon=ft.Icons.HOME,
                label_content=ft.Text("Home")
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.WEB,
                label_content=ft.Text("Direcciones Web")
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.CREDIT_CARD,
                label_content=ft.Text("Tarjetas")
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.NOTES,
                label_content=ft.Text("Notas Seguras")
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.VERIFIED_USER,
                label_content=ft.Text("Acerca de")
            )
        ]


