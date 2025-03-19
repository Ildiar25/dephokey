from sqlalchemy.orm import relationship

from .creditcard import CreditCard
from .note import Note
from .password_request import PasswordRequest
from .site import Site
from .user import User


def user_relationships() -> None:
    User.creditcards = relationship(
        argument=CreditCard,
        back_populates="user",
        cascade="all, delete",
        lazy="selectin"
    )
    User.notes = relationship(
        argument=Note,
        back_populates="user",
        cascade="all, delete",
        lazy="selectin"
    )
    User.password_requests = relationship(
        argument=PasswordRequest,
        back_populates="user",
        cascade="all, delete",
        lazy="selectin"
    )
    User.sites = relationship(
        argument=Site,
        back_populates="user",
        cascade="all, delete",
        lazy="selectin"
    )
