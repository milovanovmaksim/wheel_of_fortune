from dataclasses import dataclass

import yaml


@dataclass
class VkApiConfig:
    access_token: str
    group_id: str
    host: str = "https://api.vk.com/method/"


def setup_config(config_path: str) -> VkApiConfig:
    with open(config_path, "r") as f:
        raw_config = yaml.safe_load(f)

    access_token = raw_config["bot"]["access_token"]
    group_id = raw_config["bot"]["group_id"]
    vk_api_config = VkApiConfig(access_token=access_token, group_id=group_id)
    return vk_api_config
