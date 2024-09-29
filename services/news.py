from .base import Service
from repositories import NewsRepository
from schemas import CreateNews, EditNews
from models import News

from fastapi.exceptions import HTTPException
from starlette import status


class NewsService(Service):
    repository: NewsRepository

    async def create_news(self, news: CreateNews, user_id: int):
        return await self.repository.create(news, user_id)

    async def get_news(self, news_id: int, user_id: int):
        news = await self.repository.get_by_id(news_id)
        if news is None or (
                news.is_private and news.author_id != user_id
        ) or news.archived:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='News not found'
            )
        await self.repository.watch_news(news)
        return news

    async def archive_news(self, news_id: int, user_id: int):
        news = await self.repository.get_by_id(news_id)
        if news.author_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='You are not allowed to archive this news'
            )
        return await self.repository.archive_news(news)

    async def edit_news(self, news_id: int, data: EditNews, user_id: int):
        news = await self.repository.get_by_id(news_id)
        if news.author_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='You are not allowed to edit this news'
            )
        return await self.repository.edit_news(news, data)

    async def get_public_and_mine_news(self, user_id: int):
        return await self.repository.get_public_and_mine_news(user_id)
