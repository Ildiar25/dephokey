import flet as ft

from data.db_orm import Base, engine, session

from features.models.user import UserRole, User
from features.email_management.email import Email
from features.encryption.core import encrypt_data

from interface.pages import *
from interface.controls.my_footer import Footer

from shared.utils.colors import *
from shared.logger_setup import main_logger as logger
from shared.generators import GenerateToken


def create_admin_account() -> None:
    admin = User(fullname="Administrador", email="admin.24@gmail.com", password="Admin1234", user_role=UserRole.ADMIN)
    session.add(admin)
    session.commit()


def main(page: ft.Page) -> None:

    # Create all tables
    Base.metadata.create_all(bind=engine)
    logger.info("¡BASE DE DATOS cargada con éxito!")

    # Add admin user automatically
    if not session.query(User).filter(User.email == "admin.24@gmail.com").first():
        create_admin_account()

    # This snippet allows change UserRole without any bug (DELETE AFTER FINISH THE APP)
    user = User("Usuario Prueba", "test@test.com", "test1234", UserRole.ADMIN)
    page.session.set("session", user)

    # Page settings
    page.title = "Dephokey"
    page.fonts = {
        "AlbertSansR": "interface/assets/fonts/albert-sans/albert-sans-regular.ttf",
        "AlbertSansB": "interface/assets/fonts/albert-sans/albert-sans-bold.ttf",
        "AlbertSansL": "interface/assets/fonts/albert-sans/albert-sans-light.ttf"
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
            page.add(Home(page))
            logger.info("Página HOME cargada.")

    # Define routes
    page.on_route_change = route_changer
    page.go("/home")  # Change to 'login' once program is finished

    # Testing email module (DELETE AFTER FINISH THE APP)
    code_encrypted = encrypt_data(GenerateToken.tokenize())

    new_email = Email(user, code_encrypted)
    print(new_email.message_content)

if __name__ == '__main__':
    ft.app(target=main, assets_dir="interface/assets")
