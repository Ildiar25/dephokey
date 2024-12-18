from datetime import date

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from data.db_orm import Base

from features.models.user import User
# from features.encrypter import encrypt_data

from shared.public_id import PublicID
from shared.logger_setup import test_logger as logger


class CreditCard(Base):
    """
    This class creates a new creditcard instance. It needs an ID, a UserID, a Cardholder, a Number,
    a CVC, an ExpiresDate, an Alias and a CreatedDate.
    """

    # Table settings
    __tablename__: str = "creditcard"

    # Column settings
    id: Mapped[str] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), nullable=False, index=True)
    cardholder: Mapped[str]
    encrypted_number: Mapped[str]
    encrypted_cvc: Mapped[str]
    valid_until: Mapped[date]
    expired: Mapped[bool]
    alias: Mapped[str | None]
    created: Mapped[date]

    # Relationship settings
    user: Mapped["User"] = relationship("User", back_populates="creditcards")

    # Initializer
    def __init__(self, cardholder: str, number: str, cvc: str, valid_until: date,
                 user: User, alias: str | None = None) -> None:
        super().__init__()

        self.id: str = PublicID.generate_short_id()
        self.cardholder: str = cardholder
        self.encrypted_number: str = number  # encrypt_data(number)
        self.encrypted_cvc: str = cvc  # encrypt_data(number)
        self.valid_until: date = valid_until
        self.user: User = user
        self.expired: bool = True if self.valid_until < date.today() else False
        self.alias: str = alias
        self.created: date = date.today()

        # Logs new creditcard
        logger.info("Creditcard instance created!")

    def __str__(self) -> str:
        return (f"<class Creditcard(id='{self.id}', cardholder='{self.cardholder}', encrypted_number={str}, "
                f"encrypted_cvc={str}, valid_until='{self.valid_until.strftime("%d/%m/%Y")}', expired={self.expired}, "
                f"alias='{self.alias}', created='{self.created.strftime("%d/%m/%Y")}')>")
