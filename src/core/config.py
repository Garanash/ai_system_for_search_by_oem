from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class RunConfig(BaseModel):
    host: str = '127.0.0.1'
    port: int = 8000


class ApiV1Prefix(BaseModel):
    prefix: str = '/v1'
    users: str = '/users'
    metiz: str = '/metiz'
    RWD: str = '/RWD'
    project: str = "/project"
    purchased: str = '/purchased'
    purchasedHydro: str = '/hydroperfs'
    according: str = '/draw'
    adaptersAndPlugs: str = '/adapters'


class ApiPrefix(BaseModel):
    prefix: str = '/api'
    v1: ApiV1Prefix = ApiV1Prefix()


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }


class Token(BaseModel):
    token:str

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="AGB_APP__"
    )
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    db: DatabaseConfig
    gpt: Token


settings = Settings()

# если есть желание проверить данные из .env файла
# print(settings.db.url)
# print(settings.gpt.token)
