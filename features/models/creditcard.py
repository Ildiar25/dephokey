from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from data.db_orm import Base

from features.models.user import User
# from features.encryption_module import encrypt_data

from shared.utils.masker import mask_text, mask_email
from shared.generators import GenerateID
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
    valid_until: Mapped[datetime]
    expired: Mapped[bool]
    alias: Mapped[str | None]
    created: Mapped[datetime]

    # Relationship settings
    user: Mapped["User"] = relationship("User", back_populates="creditcards")

    # Initializer
    def __init__(self, cardholder: str, number: str, cvc: str, valid_until: datetime,
                 user: User, alias: str | None = None) -> None:
        super().__init__()

        self.id: str = GenerateID.short_id()
        self.cardholder: str = cardholder
        self.encrypted_number: str = number  # encrypt_data(number)
        self.encrypted_cvc: str = cvc  # encrypt_data(number)
        self.valid_until: datetime = valid_until
        self.expired: bool = True if self.valid_until < datetime.today() else False
        self.alias: str | None = alias
        self.user: User = user
        self.created: datetime = datetime.today()

        # Logs new creditcard
        logger.info("Creditcard instance created!")

    def __str__(self) -> str:
        return (f"<class Creditcard(id='{self.id}', cardholder='{self.cardholder}', "
                f"encrypted_number={mask_text(self.encrypted_number)}, encrypted_cvc={mask_text(self.encrypted_cvc)}, "
                f"valid_until='{self.valid_until.strftime('%Y-%m-%d')}', expired={self.expired}, alias='{self.alias}', "
                f"user={mask_email(self.user.email)}, created='{self.created.strftime('%Y-%m-%dT%H:%M:%S')}')>")
