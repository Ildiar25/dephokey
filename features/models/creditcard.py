from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Boolean

from data.db_orm import Base

from features.models.user import User
from features.data_encryption.core import encrypt_data

from shared.utils.masker import mask_text, mask_email
from shared.generators import GenerateID
from shared.logger_setup import test_log as log


class CreditCard(Base):
    """
    This class creates a new creditcard instance. It needs an ID, a UserID, a Cardholder, a Number,
    a CVC, an ExpiresDate, an Alias and a CreatedDate.
    """

    # Table settings
    __tablename__: str = "creditcard"

    # Column settings
    id: Mapped[str] = mapped_column(String(15), primary_key=True)
    user_id: Mapped[str] = mapped_column(
        String(15), ForeignKey(column="user.id", ondelete="CASCADE"), nullable=False, index=True)
    cardholder: Mapped[str] = mapped_column(String(250))
    encrypted_number: Mapped[str] = mapped_column(String(4100))
    encrypted_cvc: Mapped[str] = mapped_column(String(4100))
    valid_until: Mapped[datetime]
    expired: Mapped[bool] = mapped_column(Boolean())
    alias: Mapped[str | None] = mapped_column(String(250))
    created: Mapped[datetime]

    # Relationship settings
    user: Mapped["User"] = relationship(argument="User", back_populates="creditcards")

    # Initializer
    def __init__(self, cardholder: str, number: str, cvc: str, valid_until: datetime,
                 user: "User", alias: str | None = None) -> None:
        super().__init__()

        self.id: str = GenerateID.short_id()
        self.cardholder: str = cardholder
        self.encrypted_number: str = encrypt_data(number)
        self.encrypted_cvc: str = encrypt_data(cvc)
        self.valid_until: datetime = valid_until
        self.expired: bool = False
        self.alias: str | None = alias
        self.user: "User" = user
        self.created: datetime = datetime.today()

        self.update_expired()

        # Logs new creditcard
        log.info(f"Instancia de CREDITCARD creada por {repr(mask_email(self.user.email))}.")

    def __update_alias(self) -> None:
        if self.alias is not None:
            if self.expired and " (caducada)" not in self.alias:
                self.alias += " (caducada)"
            else:
                self.alias = self.alias.replace(" (caducada)", "")

    def update_expired(self) -> None:
        self.expired = self.valid_until < datetime.today()
        self.__update_alias()

    def __str__(self) -> str:
        return (f"<class Creditcard(id={repr(self.id)}, cardholder={repr(self.cardholder)}, "
                f"encrypted_number={repr(mask_text(self.encrypted_number))}, encrypted_cvc"
                f"={repr(mask_text(self.encrypted_cvc))}, valid_until={repr(self.valid_until.strftime('%Y-%m'))}, "
                f"expired={repr(self.expired)}, alias={repr(self.alias)}, user={repr(mask_email(self.user.email))}, "
                f"created={repr(self.created.strftime('%Y-%m-%dT%H:%M:%S'))})>")
