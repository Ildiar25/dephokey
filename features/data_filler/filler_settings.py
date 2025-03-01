from datetime import datetime
from faker import Faker

from data.db_orm import session

from features.models.user import User, UserRole
from features.models import Site, CreditCard, Note

from shared.logger_setup import main_log as log


def fill_with_data(user: User) -> None:
    log.info(f"Añadiendo elementos de prueba al usuario {user.email}...")
    fake = Faker('es_ES')
    some_sites = []
    for _ in range(10):
        some_sites.append(
            Site(address=fake.url(), username=user.email, password=fake.password(length=12),
                 user=user, name=fake.domain_name().capitalize())
        )
    session.add_all(some_sites)

    some_cards = []
    for _ in range(10):
        fake_date = fake.date_time_between(datetime(year=2020, month=1, day=1), datetime(year=2040, month=1, day=1))
        some_cards.append(
            CreditCard(
                cardholder=fake.name().title(), number=fake.credit_card_number(),
                cvc=fake.credit_card_security_code(), user=user, alias=fake.word().capitalize(),
                valid_until=fake_date
            )
        )
    session.add_all(some_cards)

    some_notes = []
    for _ in range(10):
        some_notes.append(
            Note(content=fake.text(), user=user, title=fake.name().capitalize())
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
    log.info("¡Datos de prueba creados exitosamente!")


def fill_with_users() -> None:
    # Add admin user automatically
    if not session.query(User).filter(User.email == "admin.24@gmail.com").first():
        log.info("Usuario ADMIN no encontrado. Se procede a crearlo...")
        create_admin_account()

    # Add client user automatically
    if not session.query(User).filter(User.email == "client.24@gmail.com").first():
        log.info("Usuario CLIENT no encontrado. Se procede a crearlo...")
        create_client_account()
