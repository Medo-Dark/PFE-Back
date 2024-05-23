from functools import lru_cache
from dotenv import dotenv_values
from schemas.settings import Settings, JWTSettings, MailSettings


@lru_cache
def get_settings() -> Settings:
    env_values = dotenv_values('.env')
    jwt_env_values = {k[len('JWT_'):]: v for k, v in env_values.items() if k.startswith('JWT_')}
    mail_env_values = {k[len('MAIL_'):]: v for k, v in env_values.items() if k.startswith('MAIL_')}

    # Instantiate nested settings classes implicitly
    jwt_settings = JWTSettings(**jwt_env_values)
    mail_settings = MailSettings(**mail_env_values)

    # Instantiate the top-level settings class
    settings = Settings(
        APP_HOST=env_values['APP_HOST'],
        APP_PORT=int(env_values['APP_PORT']),
        APP_FRONT_PORT=int(env_values['APP_FRONT_PORT']),
        DB_URL=env_values['DB_QRM_URL'],
        DB_DATA_URL=env_values['DB_QRM_DATA_URL'],
        JWT=jwt_settings,
        FORGET_PASSWORD_LINK_EXPIRE_MINUTES=int(env_values['FORGET_PASSWORD_LINK_EXPIRE_MINUTES']),
        MAIL=mail_settings
    )
    return settings
