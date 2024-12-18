from datetime import date
from hashlib import sha256

from sqlalchemy.orm import Mapped, mapped_column, relationship

from data.db_orm import Base

from features.models import *

from shared.public_id import PublicID
from shared.logger_setup import test_logger as logger


class User(Base):
    """
    This class creates a new user instance. It needs an UserID, a CompleteName, a Username, a Password
    and a CreatedDate.
    """

    # Table settings
    __tablename__: str = "user"

    # Column settings
    id: Mapped[str] = mapped_column(primary_key=True)
    fullname: Mapped[str]
    email: Mapped[str]
    hashed_password: Mapped[str]
    created: Mapped[date]

    # Relationship settings
    notes: Mapped[list["Note"]] = relationship("Note", back_populates="user", passive_deletes=True)
    sites: Mapped[list["Site"]] = relationship("Site", back_populates="user", passive_deletes=True)
    creditcards: Mapped[list["CreditCard"]] = relationship("CreditCard", back_populates="user",
                                                           passive_deletes=True)

    # Initializer
    def __init__(self, fullname: str, email: str, password: str) -> None:
        super().__init__()

        self.id: str = PublicID.generate_short_id()
        self.fullname: str = fullname
        self.email: str = email
        self.hashed_password: str = sha256(password.encode()).hexdigest()
        self.created: date = date.today()

        # Logs new user
        logger.info("User instance created!")

    def __str__(self) -> str:
        return (f"<class User(id='{self.id}', fullname='{self.fullname}', email={str}, "
                f"hashed_password={str}, created='{self.created.strftime("%d/%m/%Y")}')>")
