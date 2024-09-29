from .security import is_valid_token, decode_token
from services.users import UserService
from routers.auth import oauth2_scheme
from schemas import ShortUser, NewsModel, CommentModel


from fastapi import Depends
from fastapi.exceptions import HTTPException
from typing import Annotated
from starlette import status


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        user_service: UserService = Depends()
):
    try:
        data = decode_token(token)
        user = await user_service.get_by_id(data.get('id'))
        if is_valid_token(token, user):
            return user
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token is not valid anymore'
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'Token expired! {exc}'
        )


async def convert_news_schema(news, short=False):
    txt = news.description
    if short:
        txt = txt[:30] + '...'
    return NewsModel(
        id=news.id,
        title=news.title,
        description=txt,
        views=news.views,
        created=news.created_at.date(),
        edited=news.created_at.timestamp() != news.updated_at.timestamp(),
        author=ShortUser(
            id=news.author_id,
            fullname=news.author.fullname,
            email=news.author.email,
            joined=news.author.created_at.date()
        )
    )


async def convert_comments_schema(comment):
    return CommentModel(
        id=comment.id,
        news_id=comment.news_id,
        content=comment.content,
        edited=comment.created_at.timestamp() != comment.updated_at.timestamp(),
        author=ShortUser(
            id=comment.author_id,
            fullname=comment.author.fullname,
            email=comment.author.email,
            joined=comment.author.created_at.date()
        )
    )
