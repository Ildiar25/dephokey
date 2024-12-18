from datetime import date

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from data.db_orm import Base

from features.models.user import User
# from features.encrypter import encrypt_data

from shared.public_id import PublicID
from shared.logger_setup import test_logger as logger


class Note(Base):
    """
    This class creates a new note instance. It needs an ID, a UserID, a Title, a Content and a
    CreatedDate.
    """

    # Table settings
    __tablename__: str = "note"

    # Column settings
    id: Mapped[str] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), nullable=False, index=True)
    title: Mapped[str | None]
    encrypted_content: Mapped[str]
    created: Mapped[date]

    # Relationship settings
    user: Mapped["User"] = relationship("User", back_populates="notes")

    # Initializer
    def __init__(self, content: str, user: User, title: str | None = None) -> None:
        super().__init__()

        self.id: str = PublicID.generate_short_id()
        self.title: str | None = title
        self.encrypted_content = content  # encrypt_data(content)
        self.user: User = user
        self.created: date = date.today()

        # Logs new note
        logger.info("Note instance created...")

    def __str__(self) -> str:
        return (f"<classNote: id='{self.id}', title='{self.title}', "
                f"content_encrypted='{...}', user='{...}', "
                f"created='{self.created.strftime("%d/%m/%Y")}'>")
