from dataclasses import dataclass
from typing import TYPE_CHECKING


from broker.config import setup_config as setup_broker_config
from vk_api.config import setup_config as setup_vk_api_config
from store.database.config import setup_config as setup_database_config

if TYPE_CHECKING:
    from broker.config import BrokerConfig
    from vk_api.config import VkApiConfig
    from store.database.config import DatabaseConfig


@dataclass
class Config:
    vk_api_config: "VkApiConfig"
    broker_config: "BrokerConfig"
    database: "DatabaseConfig"


def setup_config(path: str):
    vk_api_config = setup_vk_api_config(path)
    broker_config = setup_broker_config(path)
    data_base_config = setup_database_config(path)
    return Config(vk_api_config, broker_config, data_base_config)
