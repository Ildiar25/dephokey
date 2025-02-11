from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from data.db_orm import Base

from features.models.user import User
# from features.encryption_module import encrypt_data

from shared.utils.masker import mask_username, mask_text
from shared.generators import GenerateID
from shared.logger_setup import test_logger as logger


class Site(Base):
    """
    This class creates a new site instance. It needs an ID, a UserID, a Name, an Address, a UserName,
    a Password and a CreatedDate.
    """

    # Table settings
    __tablename__: str = "site"

    # Column settings
    id: Mapped[str] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), nullable=False, index=True)
    name: Mapped[str | None]
    address: Mapped[str]
    username: Mapped[str]
    encrypted_password: Mapped[str]
    created: Mapped[datetime]

    # Relationship settings
    user: Mapped["User"] = relationship("User", back_populates="sites")

    # Initializer
    def __init__(self, address: str, username: str, password: str, user: User, name: str | None = None) -> None:
        super().__init__()

        self.id: str = GenerateID.short_id()
        self.name: str | None = name
        self.address: str = address
        self.username: str = username
        self.encrypted_password: str = password  # encrypt_data(password)
        self.user: User = user
        self.created: datetime = datetime.today()

        # Logs new note
        logger.info("Site instance created!")

    def __str__(self) -> str:
        return (f"<class Site(id='{self.id}', name='{self.name}', address='{self.address}', username="
                f"{mask_username(self.username)}, encrypted_password={mask_text(self.encrypted_password)}, "
                f"user={self.user.fullname}, created='{self.created.strftime('%Y-%m-%dT%H:%M:%S')}')>")
