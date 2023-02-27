import typing
from typing import Optional, List
from random import randint
from sys import maxsize
import logging

from aiohttp.client import ClientSession

from app.base.base_accessor import BaseAccessor
from app.store.vk_api.dataclasses import Message,  Update
from app.store.vk_api.poller import Poller


if typing.TYPE_CHECKING:
    from app.web.app import Application


logger = logging.getLogger()


class VkApiAccessor(BaseAccessor):
    HOST = "https://api.vk.com/method/"

    def __init__(self, app: "Application", *args, **kwargs):
        super().__init__(app, *args, **kwargs)
        self.session: Optional[ClientSession] = None
        self.key: Optional[str] = None
        self.server: Optional[str] = None
        self.poller: Optional["Poller"] = None
        self.ts: Optional[int] = None
        self.params = {
            "access_token": app.config.bot.access_token,
            "group_id": app.config.bot.group_id
        }

    async def connect(self, app: "Application"):
        self.session = ClientSession()
        await self._get_long_poll_service()
        self.poller = Poller(app.store)
        await self.poller.start()

    async def disconnect(self, app: "Application"):
        if self.poller:
            await self.poller.stop()
        if self.session:
            await self.session.close()

    @staticmethod
    def _build_query(host: str, method: str, params: dict) -> str:
        url = host + method + "?"
        if "v" not in params:
            params["v"] = "5.131"
        url += "&".join([f"{k}={v}" for k, v in params.items()])
        return url

    async def _get_long_poll_service(self):
        url: str = self._build_query(VkApiAccessor.HOST,
                                     method="groups.getLongPollServer",
                                     params=self.params)
        async with self.session.get(url) as response:
            json_data = await response.json()
        self.server = json_data["response"]["server"]
        self.key = json_data["response"]["key"]
        self.ts = json_data["response"]["ts"]

    async def poll(self) -> List[Optional[Update]]:
        url = f"{self.server}?act=a_check&key={self.key}&ts={self.ts}&wait=25"
        async with self.session.post(url) as response:
            json_data = await response.json()
        self.ts = json_data.get("ts")
        updates: List[Optional[Update]] = [Update.Schema_().load(update) for update in json_data["updates"]]
        return updates

    async def send_message(self, message: Message) -> None:
        params = {
            "user_id": message.user_id,
            "random_id": randint(0, maxsize)
        }
        params.update(self.params)
        kwargs = {
            'params': {"message": message.text}
        }
        url: str = self._build_query(VkApiAccessor.HOST, method="messages.send", params=params)
        async with self.session.post(url, **kwargs) as response:
            json_data = await response.json()
            data = {"user_id": message.user_id, "text": message.text, "response": json_data}
            logger.info(f"New meaasage for user {data}")
