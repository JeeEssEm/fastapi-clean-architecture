from pydantic import BaseModel
from .users import ShortUser


class CommentModel(BaseModel):
    id: int
    news_id: int
    content: str
    author: ShortUser
    edited: bool


class CreateComment(BaseModel):
    content: str
