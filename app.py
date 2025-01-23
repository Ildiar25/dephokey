import flet as ft

from data.db_orm import Base, engine

from features.models.user import UserRole

from interface.pages import *
from interface.controls.my_appbar import CustomAppbar
from interface.controls.my_footer import Footer

from shared.utils.colors import *
from shared.logger_setup import main_logger as logger


def main(page: ft.Page) -> None:

    # Create all tables
    Base.metadata.create_all(bind=engine)
    logger.info("BASE DE DATOS creada con éxito!")

    # Page settings
    page.title = "Dephokey"
    # page.window.maximized = True
    page.fonts = {
        "AlbertSansR": "interface/assets/fonts/albert-sans/albert-sans-regular.ttf",
        "AlbertSansB": "interface/assets/fonts/albert-sans/albert-sans-bold.ttf",
        "AlbertSansL": "interface/assets/fonts/albert-sans/albert-sans-light.ttf"
    }

    # Page design
    page.theme = ft.Theme(font_family="AlbertSansR")
    page.bgcolor = darkColorBackground
    page.padding = ft.padding.all(0)
    page.window.min_width = 950
    page.window.min_height = 650

    # Page elements
    page.appbar = CustomAppbar()
    page.bottom_appbar = Footer()

    def route_changer(_: ft.ControlEvent):
        page.clean()
        if page.route == "/login":
            page.add(Login(page))
            logger.info("Página LOGIN cargada.")

        elif page.route == "/reset_password":

            logger.info("Página RESET PASSWORD cargada.")

        elif page.route == "/signup":
            page.add(Signup(page))
            logger.info("Página SIGNUP cargada.")

        elif page.route == "/home" and page.session.contains_key("session"):
            user_role = page.session.get("session").role

            if user_role == UserRole.ADMIN:
                page.add(Admin(page))
                logger.info("Página ADMINN cargada.")

            elif user_role == UserRole.CLIENT:
                page.add(Home(page))
                logger.info("Página HOME cargada.")

        else:
            page.add(Home(page))  # Delete 'else' statement once program was finished

    # Define routes
    page.on_route_change = route_changer
    page.go("/home")  # Change to 'login' once program finished


if __name__ == '__main__':
    ft.app(target=main, assets_dir="interface/assets")
