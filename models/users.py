from datetime import date, datetime

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class User(Base):
    __tablename__ = 'users'

    phone: Mapped[str | None] = mapped_column(String(16), default=None)
    email: Mapped[str | None]
    fullname: Mapped[str | None]
    password: Mapped[str]

    verified: Mapped[bool] = mapped_column(default=False)
    avatar: Mapped[str | None]
    birthday = Mapped[date | None]
    token_valid_date: Mapped[datetime] = mapped_column(default=datetime.now())

    # employee_id: Mapped[int] = mapped_column(ForeignKey('restaurant_accounts.id'))
    # employee: Mapped["RestaurantAccount"] = relationship(back_populates='employees')
    #
    

# class RestaurantAccount(Base):
#     contact_phone: Mapped[str] = mapped_column(String(16))
#     employees: Mapped[list["User"]] = relationship(back_populates="employee")
