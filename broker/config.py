from dataclasses import dataclass

import yaml


@dataclass
class BrokerConfig:
    rabbit_url: str


def setup_config(config_path: str):
    with open(config_path, "r") as f:
        raw_config = yaml.safe_load(f)
    url: str = raw_config["rabbit"]["url"]
    return BrokerConfig(url)
