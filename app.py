import asyncio

import flet as ft

from data.db_orm import Base, main_database
from features.data_filler.filler_settings import fill_with_users
from interface.controls.footer import Footer
from interface.pages import Dashboard, Login, ResetPasswordPage, Signup
from shared.logger_setup import main_log as log
from shared.utils.colors import primaryCorporate100


async def __check_session_is_expired(page: ft.Page) -> None:
    """Monitores if session is expired every 30 seconds"""
    log.info("Monitoreo de la sesión inicializado.")
    current_session = True

    while current_session:
        await asyncio.sleep(30)
        if page.session.contains_key("session"):
            continue

        current_session = False
        await __back_to_login_page(page)


async def __back_to_login_page(page: ft.Page) -> None:
    """Navigates to login page."""
    log.info("Sesión expirada. Redirigiendo a LOGIN.")
    page.session.clear()

    if len(page.controls) != 0 and isinstance(page.controls[0], Dashboard):
        # Hide menus
        page.appbar.visible = False
        page.bottom_appbar.visible = False
        page.bgcolor = primaryCorporate100
        page.clean()
        page.update()
        page.go("/login")
        return


def main(page: ft.Page) -> None:
    # Create all tables
    Base.metadata.create_all(bind=main_database.engine)
    log.info("¡BASE DE DATOS cargada con éxito!")
    fill_with_users()

    # Page settings
    page.title = "Dephokey — PasswordManager v.0.3.3"
    page.fonts = {
        "AlbertSansR": "interface/assets/fonts/albert-sans/albert-sans-regular.ttf",
        "AlbertSansB": "interface/assets/fonts/albert-sans/albert-sans-bold.ttf",
        "AlbertSansL": "interface/assets/fonts/albert-sans/albert-sans-light.ttf",
        "AlbertSansI": "interface/assets/fonts/albert-sans/albert-sans-italic.ttf",
        "IcelandR": "interface/assets/fonts/iceland/iceland-regular.ttf",
    }

    # Page design
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = primaryCorporate100
    page.padding = ft.padding.all(0)
    page.window.min_width = 1360
    page.window.min_height = 768

    # Page behavior
    page.theme = ft.Theme(
        font_family="AlbertSansR",
        page_transitions=ft.PageTransitionsTheme(ft.PageTransitionTheme.NONE),
    )

    # Page elements
    page.bottom_appbar = Footer()

    def route_changer(_: ft.ControlEvent):
        page.clean()
        if page.route == "/login":
            log.info("Redirigiendo a LOGIN.")
            page.add(Login(page))

        elif page.route == "/reset_password":
            log.info("Redirigiendo a PW_RECOVER GENERATE_PW.")
            page.add(ResetPasswordPage(page))

        elif page.route == "/signup":
            log.info("Redirigiendo a SIGNUP.")
            page.add(Signup(page))

        elif page.route == "/home" and page.session.contains_key("session"):
            log.info("Redirigiendo a DASHBOARD")
            page.add(Dashboard(page))

            # Initializes session monitoring
            page.loop.create_task(__check_session_is_expired(page))

    # Define routes
    page.on_route_change = route_changer
    page.go("/login")


if __name__ == '__main__':
    ft.app(target=main, assets_dir="interface/assets")
