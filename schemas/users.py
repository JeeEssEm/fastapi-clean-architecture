from pydantic import BaseModel, EmailStr, field_validator, Field
import re
from datetime import date


password_exp = re.compile(
    r'^.*(?=.{8,})(?=.*[a-zA-Z])(?=.*\d)(?=.*[!#$%&? "]).*$'
)


class UserMixin(BaseModel):
    fullname: str
    email: EmailStr


class CreateUser(UserMixin):
    password1: str
    password2: str
    phone: str | None = None

    @field_validator('password1', mode='after')
    @classmethod
    def passwords_match(cls, v, info):
        if 'password2' in info.data and v != info.data['password2']:
            raise ValueError('passwords do not match')
        return v

    @field_validator('password1', mode='after')
    @classmethod
    def validate_password(cls, v):

        if not password_exp.match(v):
            raise ValueError(
                'Password must contain: at least 1 uppercase letter, '
                'special symbol and 1 digit')
        return v

    #  TODO: phone number validator


class ShortUser(UserMixin):
    id: int
    joined: date
