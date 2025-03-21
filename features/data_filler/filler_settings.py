import datetime
import random
from datetime import timedelta

from faker import Faker

from data.db_orm import session
from features.models.creditcard import CreditCard
from features.models.note import Note
from features.models.site import Site
from features.models.user import User, UserRole
from shared.logger_setup import main_log as log
from shared.validate import Validate

FAKE = Faker('es_ES')


def __test_number_validation() -> str:
    number = ""
    while not Validate.is_valid_creditcard_number(number):
        number = FAKE.credit_card_number()

    return number


def __fill_with_data(user: User) -> None:
    log.info(f"Añadiendo elementos de prueba al usuario {user.email}...")

    some_sites = []
    for _ in range(10):
        some_sites.append(
            Site(
                address=FAKE.url(),
                username=user.email,
                password=FAKE.password(length=18, special_chars=False),
                user=user,
                name=FAKE.domain_name().capitalize()
            )
        )
    session.add_all(some_sites)

    some_cards = []
    for _ in range(10):
        fake_date = FAKE.date_time_between(
            datetime.datetime.today() - timedelta(weeks=260),
            datetime.datetime.today() + timedelta(weeks=260)
        )
        some_cards.append(
            CreditCard(
                cardholder=FAKE.name().title(),
                number=__test_number_validation(),
                cvc=str(random.randint(a=100, b=9999)),
                user=user,
                alias=FAKE.word().capitalize(),
                valid_until=fake_date
            )
        )
    session.add_all(some_cards)

    some_notes = []
    for _ in range(10):
        some_notes.append(
            Note(
                content=FAKE.text(max_nb_chars=324),
                user=user,
                title=FAKE.word().capitalize()
            )
        )
    session.add_all(some_notes)

    # Save changes
    session.commit()


def __create_admin_account() -> None:
    admin = User(
        fullname="Sergio Administrativo Muñoz",
        email="admin.24@gmail.com",
        password="Admin1234",
        user_role=UserRole.ADMIN
    )
    session.add(admin)
    session.commit()


def __create_client_account() -> None:
    client = User(
        fullname="Manuel Tester García",
        email="client.24@gmail.com",
        password="Client1234",
        user_role=UserRole.CLIENT
    )
    session.add(client)
    session.commit()

    # Add client data examples
    __fill_with_data(client)
    log.info("¡Datos de prueba creados exitosamente!")


def fill_with_users() -> None:
    # Add admin user automatically
    if not session.query(User).filter(User.email == "admin.24@gmail.com").first():
        log.info("Usuario ADMIN no encontrado. Se procede a crearlo...")
        __create_admin_account()

    # Add client user automatically
    if not session.query(User).filter(User.email == "client.24@gmail.com").first():
        log.info("Usuario CLIENT no encontrado. Se procede a crearlo...")
        __create_client_account()
