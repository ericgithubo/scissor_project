from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    env_name:str = "local"
    base_url:str = "http://localhost:8000"
    db_url:str = "postgresql://postgres:ojede123@localhost/url_project"

    class config:
        env_file = ".env"

@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    print(f"loading settings for :(settings.env_name)")
    return settings