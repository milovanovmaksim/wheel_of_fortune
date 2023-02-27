from dataclasses import dataclass

import yaml


@dataclass
class DatabaseConfig:
    host: str = "localhost"
    port: int = 5432
    user: str = "maxim"
    password: str = "canada"
    database: str = "wheel_of_fortune"


def setup_config(config_path):
    with open(config_path, "r") as f:
        raw_config = yaml.safe_load(f)
    return DatabaseConfig(**raw_config["database"])
