from config import settings
from schemas import CreateUser
from core.security import get_password_hash
from models import User
from .base import Repository
from sqlalchemy import select, or_


class UsersRepository(Repository):
    async def create(self, data):
        pass

    async def get_by_id(self, user_id):
        q = select(User).where(User.id == user_id)
        return (await self.session.execute(q)).scalars().first()

    async def get_by_username(self, data):
        q = select(User).where(
            or_(User.email == data, User.fullname == data)
        )
        await self.session.execute(q)
        return (await self.session.execute(q)).scalars().first()

    async def check_exists(self, fullname, email):
        q = select(User).where(or_(
            User.email == email, User.fullname == fullname
        ))
        res = (await self.session.execute(q)).scalars()
        return res.first() is not None

    async def create_user(self, user: CreateUser):

        new_user = User(
            email=user.email,
            fullname=user.fullname,
            password=get_password_hash(user.password1),
            phone=user.phone,
            verified=settings.VERIFIED
        )
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return new_user
