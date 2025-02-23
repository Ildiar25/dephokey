from datetime import datetime, timedelta
from faker import Faker

from data.db_orm import session

from features.models.user import User, UserRole
from features.models import Site, CreditCard, Note

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


def fill_with_users() -> None:
    # Add admin user automatically
    if not session.query(User).filter(User.email == "admin.24@gmail.com").first():
        logger.info("Usuario ADMIN no encontrado. Se procede a crearlo...")
        create_admin_account()

    # Add client user automatically
    if not session.query(User).filter(User.email == "client.24@gmail.com").first():
        logger.info("Usuario CLIENT no encontrado. Se procede a crearlo...")
        create_client_account()
