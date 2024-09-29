from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from database import Base


class News(Base):
    __tablename__ = 'news'

    title: Mapped[str]
    description: Mapped[str | None]
    views: Mapped[int] = mapped_column(default=0)
    is_private: Mapped[bool] = mapped_column(default=False)
    archived: Mapped[bool] = mapped_column(default=False)
    author_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    author: Mapped['User'] = relationship(lazy='joined')
    comments: Mapped[list['Comment']] = relationship(back_populates='news',
                                                     lazy='joined')
