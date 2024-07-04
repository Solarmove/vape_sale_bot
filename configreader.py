from pydantic import PostgresDsn, field_validator, AnyUrl, Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    # Bot settings
    bot_token: str
    bot_mode: str
    # I18N
    i18n_format_key: str
    # Devs
    devs: list
    admins: list
    # DB
    postgredsn: PostgresDsn

    # NowPayments Keys
    x_api_key: str
    ipn_callback: str


    @field_validator("bot_mode")
    def validate_bot_mode(cls, values):
        if values not in ["dev", "prod"]:
            raise ValueError("Bot mode must be 'dev' or 'prod'")
        return values

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"


config = Config()  # type: ignore
