import flet as ft

from features.models.user import User
from features.models import Site

from interface.pages.widgets import SiteWidget


def main(page: ft.Page) -> None:

    page.bgcolor = ft.Colors.GREY_200
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    user = User("Cliente Prueba Test", "client.24@gmail.com", "Admin1234")
    site = Site("http://www.amazon.es/", "client.24@gmail.com", "Admin1234",
                user, "Amazon")

    new_widget = SiteWidget(site, page)

    page.add(new_widget)

if __name__ == '__main__':
    ft.app(main)
