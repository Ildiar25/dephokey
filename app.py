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


def fill_with_data(user: User) -> None:
    logger.info(f"Añadiendo elementos de prueba al usuario {user.email}...")
    fake = Faker()
    some_sites = []
    for _ in range(10):
        some_sites.append(
            Site(address=fake.url(), username=user.email, password=fake.password(
                length=8, digits=True, upper_case=True, lower_case=True
            ), user=user, name=fake.domain_name())
        )
    session.add_all(some_sites)

    some_cards = []
    for _ in range(10):
        some_cards.append(
            CreditCard(
                cardholder="Cliente Tester Morenazo", number=fake.credit_card_number(),
                cvc=fake.credit_card_security_code(), valid_until=datetime.today() + timedelta(weeks=208), user=user,
                alias="Compras")
        )
    session.add_all(some_cards)

    some_notes = []
    for _ in range(10):
        some_notes.append(
            Note(content=fake.text(), user=user, title=fake.name_male())
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

    # Add client data examples
    fill_with_data(client)
    logger.info("¡Datos de prueba creados exitosamente!")


def main(page: ft.Page) -> None:

    # Create all tables
    Base.metadata.create_all(bind=engine)
    logger.info("¡BASE DE DATOS cargada con éxito!")

    # Add admin user automatically
    if not session.query(User).filter(User.email == "admin.24@gmail.com").first():
        logger.info("Usuario ADMIN no encontrado. Se procede a crearlo...")
        create_admin_account()

    # Add client user automatically
    if not session.query(User).filter(User.email == "client.24@gmail.com").first():
        logger.info("Usuario CLIENT no encontrado. Se procede a crearlo...")
        create_client_account()

    # Page settings
    page.title = "Dephokey — PasswordManager v.0.0.3"
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
            logger.info("Página DASHBOARD cargada.")

    # Define routes
    page.on_route_change = route_changer
    page.go("/login")  # Change to 'login' once program is finished


if __name__ == '__main__':
    ft.app(target=main, assets_dir="interface/assets")
