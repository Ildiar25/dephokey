from datetime import datetime
from datetime import timedelta

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from data.db_orm import Base
from features.data_encryption.core import encrypt_data
from shared.generators import GenerateID, GenerateToken
from shared.logger_setup import main_log as log
from shared.utils.masker import mask_email, mask_text

from .user import User


class PasswordRequest(Base):
    """
    This class creates a new password request instance. It needs an ID, a UserID, and a CreatedDate.
    This class allows to change password.
    """

    # Table settings
    __tablename__: str = "password_change_request"

    # Column settings
    id: Mapped[str] = mapped_column(String(15), primary_key=True)
    user_id: Mapped[str] = mapped_column(
        String(15),
        ForeignKey(column="user.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    encrypted_code: Mapped[str] = mapped_column(String(4100))
    created: Mapped[datetime]
    expires_at: Mapped[datetime]

    # Relationship settings
    user: Mapped[User] = relationship(
        argument="User",
        back_populates="password_requests"
    )

    # Initializer
    def __init__(self, user: User) -> None:
        super().__init__()

        self.id: str = GenerateID.short_id()
        self.encrypted_code: str = encrypt_data(GenerateToken.generate())
        self.user: User = user
        self.created: datetime = datetime.today()
        self.expires_at = datetime.now() + timedelta(minutes=5)

        # Logs new note
        log.info(f"Instancia de PASSWORD REQUEST creada por {repr(mask_email(self.user.email))}.")

    def __str__(self) -> str:
        return (
            f"<class PasswordRequest("
                f"id={repr(self.id)}, "
                f"user={repr(mask_email(self.user.email))}, "
                f"encrypted_code={repr(mask_text(self.encrypted_code))}, "
                f"created={repr(self.created.strftime('%Y-%m-%dT%H:%M:%S'))}, "
                f"expires_at={repr(self.expires_at.strftime('%Y-%m-%dT%H:%M:%S'))}"
            f")>"
        )
