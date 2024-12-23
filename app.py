import flet as ft

from data.db_orm import Base, engine

from features.models.user import UserRole

from interface.pages import *
# from interface.controls import *

from shared.utils.colors import *


def main(page: ft.Page) -> None:
    # Page settings
    page.title = "Dephokey"
    page.window.maximized = True
    page.fonts = {
        "AlbertSansR": "interface/assets/fonts/albert-sans/albert-sans-regular.ttf"
    }

    # Page design
    page.theme = ft.Theme(font_family="AlbertSansR")
    page.bgcolor = darkColorBackground
    page.padding = ft.padding.all(10)
    page.window.min_width = 950
    page.window.min_height = 650

    def route_changer(_: ft.ControlEvent):
        page.clean()
        if page.route == "/login":
            page.add(Login(page))

        elif page.route == "/signup":
            print("On signup Page!")

        elif page.route == "/home" and page.session.contains_key("session"):
            user_role = page.session.get("session").role

            if user_role == UserRole.ADMIN:
                page.add(Admin(page))

            elif user_role == UserRole.CLIENT:
                pass

        else:
            page.add(Admin(page))

    # Define routes
    page.on_route_change = route_changer

    # Create all tables
    # Base.metadata.create_all(bind=engine)

    page.go("/home")


if __name__ == '__main__':
    ft.app(target=main, assets_dir="interface/assets")
