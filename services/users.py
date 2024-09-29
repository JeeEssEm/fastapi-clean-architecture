from .base import Service
from core.security import verify_password, create_tokens, decode_token
from repositories import UsersRepository
from schemas import CreateUser

from fastapi.exceptions import HTTPException
from starlette import status


class UserService(Service):
    repository: UsersRepository

    async def login_user(self, username, password):
        user = await self.repository.get_by_username(username)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='User not found')

        if not verify_password(password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Incorrect password')
        return create_tokens(user.id)

    async def create_user(self, user: CreateUser):
        if await self.repository.check_exists(user.fullname, user.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Email or name already registered'
            )
        return await self.repository.create_user(user)

    async def get_by_id(self, user_id):
        return await self.repository.get_by_id(user_id)

    async def update_token(self, token):
        try:
            data = decode_token(token)
            if data.get('type') != 'refresh':
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='Invalid token'
                )
            current_user = await self.repository.get_by_id(data.get('id'))
            tokens = create_tokens(current_user.id)
            return tokens['access_token']

        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid token'
            )
