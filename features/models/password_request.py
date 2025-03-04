from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from data.db_orm import Base

from features.models.user import User
from features.data_encryption.core import encrypt_data

from shared.utils.masker import mask_email, mask_text
from shared.generators import GenerateID
from shared.logger_setup import test_log as log


class PasswordRequest(Base):
    """
    This class creates a new password request instance. It needs an ID, a UserID, and a CreatedDate.
    This class allows to change password.
    """

    # Table settings
    __tablename__: str = "password_change_request"

    # Column settings
    id: Mapped[str] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey(column="user.id", ondelete="CASCADE"), nullable=False, index=True)
    encrypted_code: Mapped[str]
    created: Mapped[datetime]

    # Relationship settings
    user: Mapped["User"] = relationship(argument="User", back_populates="password_requests", cascade="all,delete")

    # Initializer
    def __init__(self, code: str, user: User) -> None:
        super().__init__()

        self.id: str = GenerateID.short_id()
        self.encrypted_code: str = encrypt_data(code)
        self.user: User = user
        self.created: datetime = datetime.today()

        # Logs new note
        log.info(f"Instancia de PASSWORD REQUEST creada por {repr(mask_email(self.user.email))}.")

    def __str__(self) -> str:
        return (f"<class PasswordRequest(id={repr(self.id)}, user={repr(mask_email(self.user.email))}, "
                f"encrypted_code={repr(mask_text(self.encrypted_code))},"
                f"created={repr(self.created.strftime('%Y-%m-%dT%H:%M:%S'))})>")
