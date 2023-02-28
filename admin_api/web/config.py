import typing
from dataclasses import dataclass

import yaml

from store.database.config import DatabaseConfig

if typing.TYPE_CHECKING:
    from admin_api.web.app import Application


@dataclass
class SessionConfig:
    key: str


@dataclass
class AdminConfig:
    email: str
    password: str


@dataclass
class Config:
    admin: AdminConfig
    session: SessionConfig
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
        database=DatabaseConfig(**raw_config["database"])

    )
