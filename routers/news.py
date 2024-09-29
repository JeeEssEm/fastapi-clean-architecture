from models import User, News
from core.utils import get_current_user
from services import NewsService
from schemas import CreateNews, NewsModel, ShortUser, EditNews
from core.utils import convert_news_schema, convert_comments_schema

from fastapi import APIRouter, Response, Path, Depends
from typing import Annotated

router = APIRouter(tags=['news'], prefix='/news')


@router.post('/')
async def create_news(
    current_user: Annotated[User, Depends(get_current_user)],
    form: CreateNews,
    news_service: NewsService = Depends(),
):
    news = await news_service.create_news(form, current_user.id)
    return await convert_news_schema(news)


@router.delete('/{news_id}')
async def delete_news(
        current_user: Annotated[User, Depends(get_current_user)],
        news_id: int,
        news_service: NewsService = Depends()
):
    news = await news_service.archive_news(news_id, current_user.id)
    return await convert_news_schema(news)


@router.patch('/{news_id}')
async def edit_news(
        current_user: Annotated[User, Depends(get_current_user)],
        news_id: int,
        form: EditNews,
        news_service: NewsService = Depends()
):
    news = await news_service.edit_news(news_id, form, current_user.id)
    return await convert_news_schema(news)


@router.get('/')
async def get_all_news(
        current_user: Annotated[User, Depends(get_current_user)],
        news_service: NewsService = Depends()
):
    news = await news_service.get_public_and_mine_news(current_user.id)
    res = []
    for news_obj in news:
        res.append(await convert_news_schema(news_obj, short=True))
    return res


@router.get('/{news_id}/comments')
async def get_news_comments(
        news_id: int,
        current_user: Annotated[User, Depends(get_current_user)],
        news_service: NewsService = Depends()
):
    news = await news_service.get_news(news_id, current_user.id)
    res = []
    for comment_obj in news.comments:
        res.append(await convert_comments_schema(comment_obj))
    return res


@router.get('/{news_id}', response_model=NewsModel)
async def get_news(
        news_id: int,
        current_user: Annotated[User, Depends(get_current_user)],
        news_service: NewsService = Depends(),
):
    news = await news_service.get_news(news_id, current_user.id)
    return await convert_news_schema(news)
