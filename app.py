import flet as ft
import asyncio

from data.db_orm import Base, engine

from features.data_filler.filler_settings import fill_with_users

from interface.pages import *
from interface.controls.footer import Footer

from shared.utils.colors import *
from shared.logger_setup import main_logger as logger


async def check_session_is_expired(page: ft.Page) -> None:
    """Monitores if session is expired every 30 seconds"""
    check = True
    while check:
        await asyncio.sleep(30)
        if page.session.contains_key("session"):
            continue
        check = False
        await back_to_login_page(page)


async def back_to_login_page(page: ft.Page) -> None:
    page.session.clear()

    # Hide menus
    page.appbar.visible = False
    page.bottom_appbar.visible = False
    page.bgcolor = primaryCorporate100
    page.clean()
    page.update()
    page.go("/login")


def main(page: ft.Page) -> None:

    # Create all tables
    Base.metadata.create_all(bind=engine)
    logger.info("¡BASE DE DATOS cargada con éxito!")
    fill_with_users()

    # Page settings
    page.title = "Dephokey — PasswordManager v.0.3.3"
    page.fonts = {
        "AlbertSansR": "interface/assets/fonts/albert-sans/albert-sans-regular.ttf",
        "AlbertSansB": "interface/assets/fonts/albert-sans/albert-sans-bold.ttf",
        "AlbertSansL": "interface/assets/fonts/albert-sans/albert-sans-light.ttf",
        "AlbertSansI": "interface/assets/fonts/albert-sans/albert-sans-italic.ttf",
        "IcelandR": "interface/assets/fonts/iceland/iceland-regular.ttf"
    }

    # Page design
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = primaryCorporate100
    page.padding = ft.padding.all(0)
    page.window.min_width = 950
    page.window.min_height = 650

    # Page behavior
    page.theme = ft.Theme(
        font_family="AlbertSansR", page_transitions=ft.PageTransitionsTheme(ft.PageTransitionTheme.NONE)
    )

    # Page elements
    page.bottom_appbar = Footer()

    def route_changer(_: ft.ControlEvent):
        page.clean()
        if page.route == "/login":
            page.add(Login(page))
            logger.info("Página LOGIN cargada.")

        elif page.route == "/reset_password":
            page.add(ResetPasswordPage(page))
            logger.info("Página RESET PASSWORD cargada.")

        elif page.route == "/signup":
            page.add(Signup(page))
            logger.info("Página SIGNUP cargada.")

        elif page.route == "/home" and page.session.contains_key("session"):
            page.add(Dashboard(page))

            # Initializes session monitoring
            page.loop.create_task(check_session_is_expired(page))
            logger.info("Página DASHBOARD cargada.")

    # Define routes
    page.on_route_change = route_changer
    page.go("/login")


if __name__ == '__main__':
    ft.app(target=main, assets_dir="interface/assets")
