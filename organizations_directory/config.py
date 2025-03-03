from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class DbSettings(BaseModel):
    url: str
    echo: bool = False


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_nested_delimiter="__",
        env_file=(".env"),
    )
    db: DbSettings
    api_prefix: str = "/api"
    run: RunConfig = RunConfig()
    API_KEY: str


settings = Settings()
