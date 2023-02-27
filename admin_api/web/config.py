import typing
from dataclasses import dataclass

import yaml

if typing.TYPE_CHECKING:
    from app.web.app import Application


@dataclass
class SessionConfig:
    key: str


@dataclass
class AdminConfig:
    email: str
    password: str


@dataclass
class BotConfig:
    access_token: str
    group_id: int


@dataclass
class DatabaseConfig:
    host: str = "localhost"
    port: int = 5432
    user: str = "maxim"
    password: str = "canada"
    database: str = "vk_quiz_bot"


@dataclass
class Config:
    admin: AdminConfig
    session: SessionConfig
    bot: BotConfig
    database: DatabaseConfig


def setup_config(app: "Application", config_path: str):
    with open(config_path, "r") as f:
        raw_config = yaml.safe_load(f)

    app.config = Config(
        admin=AdminConfig(
            email=raw_config["admin"]["email"],
            password=raw_config["admin"]["password"],
        ),
        session=SessionConfig(key=raw_config["session"]["key"]),
        bot=BotConfig(access_token=raw_config["bot"]["token"],
                      group_id=raw_config["bot"]["group_id"],),
        database=DatabaseConfig(**raw_config["database"])

    )
