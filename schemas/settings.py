from pydantic_settings import BaseSettings


class JWTSettings(BaseSettings):
    SECRET: str
    REFRESH_SECRET: str
    FORGET_PWD_SECRET: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    FORGET_PWD_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int
    ALGORITHM: str


class MailSettings(BaseSettings):
    FROM: str
    PASSWORD: str
    HOST: str
    PORT: int


class Settings(BaseSettings):
    APP_HOST: str
    APP_PORT: int
    APP_FRONT_PORT: int
    DB_URL: str
    DB_DATA_URL: str
    JWT: JWTSettings
    MAIL: MailSettings
    FORGET_PASSWORD_LINK_EXPIRE_MINUTES: int
