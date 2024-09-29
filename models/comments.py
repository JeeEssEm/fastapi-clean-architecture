from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Comment(Base):
    __tablename__ = 'comments'

    content: Mapped[str]
    news_id: Mapped[int] = mapped_column(ForeignKey('news.id'))
    author_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    author: Mapped['User'] = relationship(lazy='joined')
    news: Mapped['News'] = relationship(back_populates='comments',
                                        lazy='joined')
