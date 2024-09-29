from models import User
from services import CommentsService, NewsService
from core.utils import get_current_user, convert_comments_schema
from schemas import CommentModel, CreateComment

from typing import Annotated
from fastapi import APIRouter, Response, Path, Depends

router = APIRouter(tags=['comments'], prefix='/comments')


@router.post('/{news_id}')
async def create_comment(
    news_id: int,
    form: CreateComment,
    current_user: Annotated[User, Depends(get_current_user)],
    comment_service: CommentsService = Depends(),
    news_service: NewsService = Depends()
):
    # вот тут вопрос: надо проверить, что новость существует. Как это лучше всего сделать?
    news = await news_service.get_news(news_id, current_user.id)
    comment = await comment_service.create(form, current_user.id, news.id)
    return await convert_comments_schema(comment)


@router.get('/{comment_id}')
async def get_comment(
        comment_id: int,
        current_user: Annotated[User, Depends(get_current_user)],
        comment_service: CommentsService = Depends()
):
    comment = await comment_service.get_by_id(current_user.id, comment_id)
    return await convert_comments_schema(comment)


@router.delete('/{comment_id}')
async def delete_comment(
        comment_id: int,
        current_user: Annotated[User, Depends(get_current_user)],
        comment_service: CommentsService = Depends()
):
    await comment_service.delete(current_user.id, comment_id)
    return 'Comment deleted successfully'


@router.patch('/{comment_id}')
async def edit_comment(
        comment_id: int,
        form: CreateComment,
        current_user: Annotated[User, Depends(get_current_user)],
        comment_service: CommentsService = Depends()
):
    comment = await comment_service.edit(current_user.id, comment_id, form)
    return await convert_comments_schema(comment)
