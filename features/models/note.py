from datetime import datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from data.db_orm import Base
from features.data_encryption.core import encrypt_data
from shared.generators import GenerateID
from shared.logger_setup import main_log as log
from shared.utils.masker import mask_email, mask_text

from .user import User


class Note(Base):
    """
    This class creates a new note instance. It needs an ID, a UserID, a Title, a Content and a
    CreatedDate.
    """

    # Table settings
    __tablename__: str = "note"

    # Column settings
    id: Mapped[str] = mapped_column(String(15), primary_key=True)
    user_id: Mapped[str] = mapped_column(
        String(15), ForeignKey(column="user.id", ondelete="CASCADE"), nullable=False, index=True)
    title: Mapped[str | None] = mapped_column(String(250))
    encrypted_content: Mapped[str] = mapped_column(String(4100))
    created: Mapped[datetime]

    # Relationship settings
    user: Mapped["User"] = relationship(argument="User", back_populates="notes")

    # Initializer
    def __init__(self, content: str, user: "User", title: str | None = None) -> None:
        super().__init__()

        self.id: str = GenerateID.short_id()
        self.title: str | None = title
        self.encrypted_content: str = encrypt_data(content)
        self.user: "User" = user
        self.created: datetime = datetime.today()

        # Logs new note
        log.info(f"Instancia de NOTE creada por {repr(mask_email(self.user.email))}.")

    def __str__(self) -> str:
        return (f"<class Note(id={repr(self.id)}, title={repr(self.title)}, "
                f"content_encrypted={repr(mask_text(self.encrypted_content))}, "
                f"user={repr(mask_email(self.user.email))}, "
                f"created={repr(self.created.strftime('%Y-%m-%dT%H:%M:%S'))})>")
