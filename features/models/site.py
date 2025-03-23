from datetime import datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from data.db_orm import Base
from features.data_encryption.core import encrypt_data
from shared.generators import GenerateID
from shared.logger_setup import main_log as log
from shared.utils.masker import mask_email, mask_text, mask_username

from .user import User


class Site(Base):
    """
    This class creates a new site instance. It needs an ID, a UserID, a Name, an Address, a UserName,
    a Password and a CreatedDate.
    """

    # Table settings
    __tablename__: str = "site"

    # Column settings
    id: Mapped[str] = mapped_column(String(15), primary_key=True)
    user_id: Mapped[str] = mapped_column(
        String(15),
        ForeignKey(column="user.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    name: Mapped[str | None] = mapped_column(String(250))
    address: Mapped[str] = mapped_column(String(4100))
    username: Mapped[str] = mapped_column(String(250))
    encrypted_password: Mapped[str] = mapped_column(String(4100))
    created: Mapped[datetime]

    # Relationship settings
    user: Mapped[User] = relationship(
        argument="User",
        back_populates="sites"
    )

    # Initializer
    def __init__(
            self,
            address: str,
            username: str,
            password: str,
            user: User,
            name: str | None = None
    ) -> None:
        super().__init__()

        self.id: str = GenerateID.short_id()
        self.name: str | None = name
        self.address: str = address
        self.username: str = username
        self.encrypted_password: str = encrypt_data(password)
        self.user: User = user
        self.created: datetime = datetime.today()

        # Logs new note
        log.info(f"Instancia de SITE creada por {repr(mask_email(self.user.email))}.")

    def __str__(self) -> str:
        return (
            f"<class Site("
            f"id={repr(self.id)}, "
            f"name={repr(self.name)}, "
            f"address={repr(self.address)}, "
            f"username={repr(mask_username(self.username))}, "
            f"encrypted_password={repr(mask_text(self.encrypted_password))}, "
            f"user={repr(self.user.fullname)}, "
            f"created={repr(self.created.strftime('%Y-%m-%dT%H:%M:%S'))}, "
            f")>"
        )
