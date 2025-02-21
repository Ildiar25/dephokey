import flet as ft
from datetime import datetime, timedelta
from faker import Faker

from data.db_orm import Base, engine, session

from features.models.user import UserRole, User
from features.models import Site, CreditCard, Note

from interface.pages import *
from interface.controls.footer import Footer

from shared.utils.colors import *
from shared.logger_setup import main_logger as logger


def fill_data(user: User) -> None:
    fake = Faker()
    some_sites = []
    for _ in range(10):
        some_sites.append(
            Site(
                fake.url(),
                user.email,
                fake.password(8, False, True, True, True),
                user,
                fake.domain_name()
            )
        )

    session.add_all(some_sites)

    some_cards = []
    for _ in range(10):
        some_cards.append(
            CreditCard(
                "Cliente Tester Morenazo",
                fake.credit_card_number(),
                "234",
                datetime.today() + timedelta(weeks=208),
                user,
                "Compras"
            )
        )

    session.add_all(some_cards)

    some_notes = []
    for _ in range(10):
        some_notes.append(
            Note(
                fake.text(),
                user,
                fake.name_male()
            )
        )

    session.add_all(some_notes)
    session.commit()


def create_admin_account() -> None:
    admin = User(
        fullname="Jefazo Administrativo Supremo", email="admin.24@gmail.com",
        password="Admin1234", user_role=UserRole.ADMIN
    )
    session.add(admin)
    session.commit()


def create_client_account() -> None:
    client = User(
        fullname="Cliente Tester Morenazo", email="client.24@gmail.com",
        password="Client1234", user_role=UserRole.CLIENT
    )
    session.add(client)
    session.commit()

    # Add user data
    fill_data(client)


def main(page: ft.Page) -> None:

    # Create all tables
    Base.metadata.create_all(bind=engine)
    logger.info("¡BASE DE DATOS cargada con éxito!")

    # Add admin user automatically
    if not session.query(User).filter(User.email == "admin.24@gmail.com").first():
        create_admin_account()

    # Add client user automatically
    if not session.query(User).filter(User.email == "client.24@gmail.com").first():
        create_client_account()

    # Page settings
    page.title = "Dephokey — PasswordManager v.0.0.1"
    page.fonts = {
        "AlbertSansR": "interface/assets/fonts/albert-sans/albert-sans-regular.ttf",
        "AlbertSansB": "interface/assets/fonts/albert-sans/albert-sans-bold.ttf",
        "AlbertSansL": "interface/assets/fonts/albert-sans/albert-sans-light.ttf",
        "AlbertSansI": "interface/assets/fonts/albert-sans/albert-sans-italic.ttf",
    }

    # Page design
    page.theme = ft.Theme(font_family="AlbertSansR")
    page.bgcolor = primaryCorporate100
    page.padding = ft.padding.all(0)
    page.window.min_width = 950
    page.window.min_height = 650

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
            logger.info("Página DASHBOARD cargada.")

    # Define routes
    page.on_route_change = route_changer
    page.go("/login")  # Change to 'login' once program is finished


if __name__ == '__main__':
    ft.app(target=main, assets_dir="interface/assets")
