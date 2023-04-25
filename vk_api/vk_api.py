from dataclasses import asdict
from random import randint
from sys import maxsize
from typing import TYPE_CHECKING, Any, Optional, Dict

from aiohttp import ClientSession

from vk_api.dcs import User
from .utils import build_query


if TYPE_CHECKING:
    from config import VkApiConfig
    from dcs import Message


class VkApi:
    def __init__(self, vk_api_config: "VkApiConfig") -> None:
        self.vk_api_config = vk_api_config
        self.session = ClientSession()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    @property
    def params(self) -> Dict[str, str]:
        return {
            "access_token": self.vk_api_config.access_token,
            "group_id": self.vk_api_config.group_id
        }

    async def send_message(self, message: "Message") -> Dict[str, Any]:
        params: Dict[str, Any] = {
            "user_id": message.user_id,
            "random_id": randint(0, maxsize)
        }
        params.update(self.params)
        kwargs = {
            'params': asdict(message)
        }
        url: str = build_query(self.vk_api_config.host, method="messages.send", params=params)
        async with self.session.post(url, **kwargs) as response:
            json_data = await response.json()
            data = {"user_id": message.user_id, "text": message.message, "response": json_data}
            return data

    async def get_user(self, id_: int) -> Optional[User]:
        user: Optional[User] = None
        params = {
            "user_ids": str(id_),
            "access_token": self.vk_api_config.access_token
        }
        url: str = build_query(self.vk_api_config.host,
                               method="users.get",
                               params=params)
        async with self.session.get(url) as response:
            json_data = await response.json()
        if json_data.get("response"):
            data: Dict[str, Any] = json_data.get("response")[0]
            first_name: Optional[str] = data.get("first_name")
            last_name: Optional[str] = data.get("last_name")
            if first_name and last_name:
                user = User(first_name, last_name)
        return user
