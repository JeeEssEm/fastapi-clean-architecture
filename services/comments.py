from .base import Service
from repositories import CommentsRepository
from schemas import CreateComment
from exceptions import NewsNotFound, CommentAccessDenied


class CommentsService(Service):
    repository: CommentsRepository

    async def create(self, data: CreateComment, user_id: int, news_id: int):
        return await self.repository.create(data, user_id, news_id)

    async def get_by_id(self, user_id: int, comment_id: int):
        comment = await self.repository.get_by_id(comment_id)
        if not comment.news.archived and (
                not comment.news.is_private or comment.news.author_id == user_id
        ):
            return comment
        raise CommentAccessDenied

    async def delete(self, user_id: int, comment_id: int):
        comment = await self.repository.get_by_id(comment_id)
        if comment.author_id != user_id:
            raise CommentAccessDenied
        if comment.news.archived or (
                comment.news.is_private and comment.news.author_id != user_id):
            raise NewsNotFound
        await self.repository.delete(comment)

    async def edit(self, user_id: int, comment_id: int, data: CreateComment):
        comment = await self.repository.get_by_id(comment_id)
        if comment.author_id != user_id:
            raise CommentAccessDenied
        if comment.news.archived or (
                comment.news.is_private and comment.news.author_id != user_id):
            raise NewsNotFound
        return await self.repository.edit_comment(comment, data)
