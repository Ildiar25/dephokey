from datetime import datetime
from enum import Enum
from hashlib import sha256

from sqlalchemy.orm import Mapped, mapped_column, relationship

from data.db_orm import Base

from features.models import *

from shared.utils.masker import mask_email, mask_text
from shared.generators import GenerateID
from shared.logger_setup import test_logger as logger


class UserRole(Enum):
    CLIENT = "client"
    ADMIN = "admin"


class User(Base):
    """
    This class creates a new user instance. It needs an UserID, a Role, a CompleteName, a Username, a Password
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
    created: Mapped[datetime]

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
        self.created: datetime = datetime.today()

        # Logs new user
        logger.info("User instance created!")

    def __str__(self) -> str:
        return (f"<class User(id={repr(self.id)}, role={repr(self.role)}, fullname={repr(self.fullname)}, "
                f"email={repr(mask_email(self.email))}, hashed_password={repr(mask_text(self.hashed_password))}, "
                f"created={repr(self.created.strftime('%Y-%m-%dT%H:%M:%S'))})>")
