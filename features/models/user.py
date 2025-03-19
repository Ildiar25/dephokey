from datetime import datetime
from enum import Enum
from hashlib import sha256

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from data.db_orm import Base
from shared.generators import GenerateID
from shared.logger_setup import main_log as log
from shared.utils.masker import mask_email, mask_text


class UserRole(Enum):
    CLIENT = "client"
    ADMIN = "admin"


class User(Base):
    """
    This class creates a new user instance. It needs an UserID, a Role, a CompleteName, a Username, a Password
    and a CreatedDate.
    """

    # Table settings
    __tablename__: str = "user"

    # Column settings
    id: Mapped[str] = mapped_column(String(15), primary_key=True)
    role: Mapped[UserRole]
    fullname: Mapped[str] = mapped_column(String(250))
    email: Mapped[str] = mapped_column(String(250))
    hashed_password: Mapped[str] = mapped_column(String(100))
    created: Mapped[datetime]

    # Initializer
    def __init__(self, fullname: str, email: str, password: str, user_role: UserRole = UserRole.CLIENT) -> None:
        super().__init__()

        self.id: str = GenerateID.short_id()
        self.role: UserRole = user_role
        self.fullname: str = fullname
        self.email: str = email
        self.hashed_password: str = sha256(password.encode()).hexdigest()
        self.created: datetime = datetime.today()

        # Logs new user
        log.info(f"Instancia de USER creada por {repr(mask_email(self.email))}.")

    def __str__(self) -> str:
        return (
            f"<class User("
                f"id={repr(self.id)}, "
                f"role={repr(self.role)}, "
                f"fullname={repr(self.fullname)}, "
                f"email={repr(mask_email(self.email))}, "
                f"hashed_password={repr(mask_text(self.hashed_password))}, "
                f"created={repr(self.created.strftime('%Y-%m-%dT%H:%M:%S'))}, "
            f")>"
        )
