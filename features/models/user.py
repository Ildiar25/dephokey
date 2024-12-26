from datetime import date
from enum import Enum
from hashlib import sha256

from sqlalchemy.orm import Mapped, mapped_column, relationship

from data.db_orm import Base

from features.models import *

from shared.public_id import GenerateID
from shared.logger_setup import test_logger as logger


class UserRole(Enum):
    CLIENT = "client"
    ADMIN = "admin"


class User(Base):
    """
    This class creates a new user instance. It needs an UserID, a CompleteName, a Username, a Password
    and a CreatedDate.
    """

    # Table settings
    __tablename__: str = "user"

    # Column settings
    id: Mapped[str] = mapped_column(primary_key=True)
    role: Mapped[UserRole]
    fullname: Mapped[str]
    email: Mapped[str]
    hashed_password: Mapped[str]
    created: Mapped[date]

    # Relationship settings
    notes: Mapped[list["Note"]] = relationship("Note", back_populates="user", passive_deletes=True)
    sites: Mapped[list["Site"]] = relationship("Site", back_populates="user", passive_deletes=True)
    creditcards: Mapped[list["CreditCard"]] = relationship("CreditCard", back_populates="user",
                                                           passive_deletes=True)
    password_change_requests: Mapped[list["PasswordRequest"]] = relationship("PasswordRequest",
                                                                             back_populates="user",
                                                                             passive_deletes=True)

    # Initializer
    def __init__(self, fullname: str, email: str, password: str, user_role: UserRole = UserRole.CLIENT) -> None:
        super().__init__()

        self.id: str = GenerateID.short_id()
        self.role: UserRole = user_role
        self.fullname: str = fullname
        self.email: str = email
        self.hashed_password: str = sha256(password.encode()).hexdigest()
        self.created: date = date.today()

        # Logs new user
        logger.info("User instance created!")

    def __str__(self) -> str:
        return (f"<class User(id='{self.id}', role='{self.role}', fullname='{self.fullname}', email={str}, "
                f"hashed_password={str}, created='{self.created.strftime("%d/%m/%Y")}')>")
