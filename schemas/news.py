from pydantic import BaseModel, Field
from datetime import date
from .users import ShortUser


class NewsMixin(BaseModel):
    title: str
    description: str


class CreateNews(NewsMixin):
    is_private: bool = Field(default=False)


class NewsModel(NewsMixin):
    id: int
    created: date
    views: int
    author: ShortUser
    edited: bool


class EditNews(BaseModel):
    title: str | None = Field(default=None)
    description: str | None = Field(default=None)
    is_private: bool | None = Field(default=None)
