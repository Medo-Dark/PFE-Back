from datetime import timedelta
from enum import Enum
from typing import Optional, List
import typing
from pydantic import BaseModel




############################################################
class UserEmail(BaseModel):
    email: str

    class Config:
        from_attributes = True


class RolesEnum(str, Enum):
    REQUESTOR = 'Requestor'
    BUYER = 'Buyer'
    ADMIN = 'Admin'


class UserBase(BaseModel):
    username: str
    email: str
    role: RolesEnum
    account_status: Optional[bool] = False


class UserInDb(UserBase):
    hashed_password: str


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None
    username: Optional[str] = None
    account_status: Optional[bool] = None
    password: Optional[str] = None



class User(UserBase):
    id: int


class UserInPut(UserBase):
    id: Optional[int] = 0
    password:str





class RefreshToken(BaseModel):
    refresh_token: str
    token_type: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenCreationSettings(BaseModel):
    to_encode: typing.Any
    key: str
    expiry: timedelta
    algorithm: str

    class Config:
        arbitrary_types_allowed = True


class TokenVerificationSettings(BaseModel):
    token: str
    key: str
    algorithm: str


class LoginRequest(BaseModel):
    username: str
    password: str


class ForgetPasswordRequest(BaseModel):
    email: str


class ResetPasswordTokenVerificationRequest(BaseModel):
    token: str


class ResetPasswordRequest(BaseModel):
    email: str
    new_password: str
    confirm_password: str

