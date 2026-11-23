from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parents[1].resolve()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env")

    llm_base_url: str
    llm_api_key: str
    llm_model: str
    data_dir: Path = BASE_DIR / "data"


settings = Settings()
