from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from data.db_orm import Base

from features.models.user import User

from shared.public_id import GenerateID
from shared.logger_setup import test_logger as logger


class PasswordRequest(Base):
    """
    This class creates a new password request instance. It needs an ID, a UserID, and a CreatedDate.
    This class allows to change password.
    """

    # Table settings
    __tablename__: str = "password_change_request"

    # Column settings
    id: Mapped[str] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), nullable=False, index=True)
    created: Mapped[datetime]

    # Relationship settings
    user: Mapped["User"] = relationship("User", back_populates="password_change_requests")

    # Initializer
    def __init__(self, user: User) -> None:
        super().__init__()

        self.id: str = GenerateID.short_id()
        self.user: User = user
        self.created: datetime = datetime.today()

        # Logs new note
        logger.info("PasswordRequest instance created!")

    def __str__(self) -> str:
        return (f"<class PasswordRequest(id='{self.id}', user={User}, "
                f"created='{self.created.strftime('%Y-%m-%dT%H:%M:%S')}')>")
