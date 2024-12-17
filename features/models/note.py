from datetime import date

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from data.db_orm import Base

# from features.models import user as us

# from features.encrypter import encrypt_data

from shared.public_id import PublicID


class Note(Base):
    """
    This class creates a new note instance. It needs an ID, a UserID, a Title, a Content and a
    CreatedDate.
    """

    # Table settings
    __tablename__ = "note"

    # Column settings
    id: Mapped[str] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), nullable=False, index=True)
    title: Mapped[str | None]
    content_encrypted: Mapped[str]
    created: Mapped[date]

    # Relationship settings
    # user: Mapped["us.User"] = relationship("User", back_populates="notes")

    # Initializer
    def __init__(self, title: str | None, content: str, user) -> None:
        super().__init__()

        self.id: str = PublicID.generate_short_id()
        self.title: str | None = title
        self.content_encrypted = content # encrypt_data(content)
        self.user: us.User = user
        self.created: date = date.today()

    def __str__(self) -> str:
        return (f"class Note: id='{self.id}', title='{self.title}', "
                f"content_encrypted='{self.content_encrypted}', user='{self.user}', "
                f"created='{self.created.strftime("%d/%m/%Y")}'.")
