from .base import Repository
from models import Comment
from schemas import CreateComment
from exceptions import CommentNotFound

from sqlalchemy import select


class CommentsRepository(Repository):
    async def create(self, data: CreateComment, user_id: int, news_id: int):
        comment = Comment(
            content=data.content,
            author_id=user_id,
            news_id=news_id
        )
        self.session.add(comment)
        await self.session.commit()
        await self.session.refresh(comment)
        return comment

    async def get_by_id(self, comment_id: int):
        q = select(Comment).where(Comment.id == comment_id)
        res = (await self.session.execute(q)).scalars().first()
        if not res:
            raise CommentNotFound
        return res

    async def delete(self, comment: Comment):
        await self.session.delete(comment)
        await self.session.commit()

    async def edit_comment(self, comment: Comment, data: CreateComment):
        comment.content = data.content
        self.session.add(comment)
        await self.session.commit()
        await self.session.refresh(comment)
        return comment
