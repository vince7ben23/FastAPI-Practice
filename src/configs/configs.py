import os
from typing import Union

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    ENV: Union[str, None] = os.getenv("ENV", "dev")


class GlobalConfig(Config):
    DATABASE_URL: Union[str, None] = None
    DB_FORCE_ROLL_BACK: bool = False


class DevConfig(GlobalConfig):
    model_config = SettingsConfigDict(env_file="src/configs/.env.dev")


class RunTestCasesConfig(GlobalConfig):
    model_config = SettingsConfigDict(env_file="src/configs/.env.runtestcases")
    DB_FORCE_ROLL_BACK: bool = True


class ProdConfig(GlobalConfig):
    model_config = SettingsConfigDict(env_file="src/configs/.env.prod")


def get_config(env: str):
    configs = {
        "dev": DevConfig,
        "run_test_cases": RunTestCasesConfig,
        "prod": ProdConfig,
    }
    return configs[env]()


config = get_config(Config().ENV)
print(config)
