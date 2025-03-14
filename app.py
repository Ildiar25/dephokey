import flet as ft
import asyncio

from data.db_orm import Base, engine

from features.data_filler.filler_settings import fill_with_users

from interface.pages import *
from interface.controls.footer import Footer

from shared.utils.colors import *
from shared.logger_setup import main_log as log


async def check_session_is_expired(page: ft.Page) -> None:
    """Monitores if session is expired every 30 seconds"""
    log.info("Monitoreo de la sesión inicializado.")
    current_session = True
    while current_session:
        await asyncio.sleep(30)
        if page.session.contains_key("session"):
            continue
        current_session = False
        await back_to_login_page(page)


async def back_to_login_page(page: ft.Page) -> None:
    log.info("Sesión expirada. Redirigiendo a LOGIN.")
    page.session.clear()

    if len(page.controls) != 0:
        if isinstance(page.controls[0], Dashboard):
            # Hide menus
            page.appbar.visible = False
            page.bottom_appbar.visible = False
            page.bgcolor = primaryCorporate100
            page.clean()
            page.update()
            page.go("/login")
            return

        page.go("/login")


def main(page: ft.Page) -> None:

    # Create all tables
    Base.metadata.create_all(bind=engine)
    log.info("¡BASE DE DATOS cargada con éxito!")
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
            log.info("Redirigiendo a LOGIN.")
            page.add(Login(page))

        elif page.route == "/reset_password":
            log.info("Redirigiendo a RESET PASSWORD.")
            page.add(ResetPasswordPage(page))

        elif page.route == "/signup":
            log.info("Redirigiendo a SIGNUP.")
            page.add(Signup(page))

        elif page.route == "/home" and page.session.contains_key("session"):
            log.info("Redirigiendo a DASHBOARD")
            page.add(Dashboard(page))

            # Initializes session monitoring
            page.loop.create_task(check_session_is_expired(page))

    # Define routes
    page.on_route_change = route_changer
    page.go("/login")


if __name__ == '__main__':
    ft.app(target=main, assets_dir="interface/assets")
