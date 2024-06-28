from datetime import datetime, timezone, timedelta
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session
import consts.static_exceptions as exceptions
from config.settings import Settings, get_settings, JWTSettings
from config.dependencies import get_db
from repositories.user_repo import UserRepository
from schemas.user import User, TokenCreationSettings, TokenVerificationSettings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

user_repository = UserRepository()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")



def create_token(sett: TokenCreationSettings):
    expire = datetime.now(timezone.utc) + sett.expiry
    sett.to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        sett.to_encode,
        sett.key,
        algorithm=sett.algorithm
    )
    return encoded_jwt


def create_reset_password_token(email: str, settings: JWTSettings):
    to_encode = {"sub": email}

    sett = TokenCreationSettings(
        to_encode=to_encode,
        key=settings.FORGET_PWD_SECRET,
        expiry=timedelta(minutes=int(settings.FORGET_PWD_EXPIRE_MINUTES)),
        algorithm=settings.ALGORITHM
    )
    return create_token(sett=sett)


async def verify_token(sett: TokenVerificationSettings):
    try:

        payload = jwt.decode(
            token=sett.token,
            key=sett.key,
            algorithms=[sett.algorithm]
        )

        username: str = payload.get("sub")
        return username
    except JWTError:
        raise exceptions.invalid_token


# Generate access and refresh tokens
def generate_tokens(user: User, settings: JWTSettings):
    access_token_expires = timedelta(minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token_expires = timedelta(minutes=int(settings.REFRESH_TOKEN_EXPIRE_MINUTES))

    to_encode = {
        "sub": user.username,
        'role': user.role,
        'email': user.email,
        'id':   user.id
    }

    access_token_sett = TokenCreationSettings(
        to_encode=to_encode,
        key=settings.SECRET,
        expiry=access_token_expires,
        algorithm=settings.ALGORITHM
    )

    refresh_token_sett = TokenCreationSettings(
        to_encode=to_encode,
        key=settings.REFRESH_SECRET,
        expiry=refresh_token_expires,
        algorithm=settings.ALGORITHM
    )

    access_token = create_token(access_token_sett)
    refresh_token = create_token(refresh_token_sett)

    return [access_token, refresh_token]


def get_user_by_email(email: str, db: Session = Depends(get_db)):
    user = user_repository.find_by_username_or_email(db=db, email=email)
    if user is None:
        raise exceptions.invalid_email
    return user


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        settings: Settings = Depends(get_settings),
        db: Session = Depends(get_db)
):
    sett = TokenVerificationSettings(
        token=token,
        key=settings.JWT.SECRET,
        algorithm=settings.JWT.ALGORITHM
    )
    username = await verify_token(sett)
    if username is None:
        raise exceptions.invalid_token
    user = user_repository.find_by_username_or_email(username=username, db=db)

    if user is None:
        raise exceptions.incorrect_credentials
    return user


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)
