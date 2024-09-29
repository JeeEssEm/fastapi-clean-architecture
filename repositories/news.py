from .base import Repository
from schemas import CreateNews, EditNews
from models import News
from exceptions import NewsNotFound

from sqlalchemy import select, or_, and_


class NewsRepository(Repository):
    async def create(self, news: CreateNews, user_id: int):
        new_news = News(
            title=news.title,
            description=news.description,
            is_private=news.is_private,
            author_id=user_id
        )
        self.session.add(new_news)
        await self.session.commit()
        await self.session.refresh(new_news)
        return new_news

    async def get_by_id(self, news_id: int):
        q = select(News).where(News.id == news_id)
        res = (await self.session.execute(q)).scalars().first()
        if not res:
            raise NewsNotFound
        return res

    async def watch_news(self, news: News):
        news.views += 1
        self.session.add(news)
        await self.session.commit()

    async def archive_news(self, news: News):
        news.archived = True
        self.session.add(news)
        await self.session.commit()
        await self.session.refresh(news)
        return news

    async def edit_news(self, news: News, data: EditNews):
        news.title = data.title or news.title
        news.description = data.description or news.description
        news.is_private = data.is_private or news.is_private
        self.session.add(news)
        await self.session.commit()
        await self.session.refresh(news)
        return news

    async def get_public_and_mine_news(self, user_id: int):
        q = select(News).where(or_(
         News.is_private == False,
         and_(News.author_id == user_id, News.archived == False)
        ))
        res = (await self.session.execute(q)).unique()
        return res.scalars().all()  # TODO: pagination
