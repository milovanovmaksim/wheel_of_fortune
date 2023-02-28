import asyncio
from typing import Optional, List, TYPE_CHECKING

from aiohttp.client import ClientSession

from bot_long_poll.dcs import Update
from vk_api.utils import build_query


if TYPE_CHECKING:
    from vk_api.config import VkApiConfig
    from bot_long_poll.poller_client import PollerClient


class PollerBaseException(Exception):
    pass


class Poller:
    def __init__(self, vk_api_config: "VkApiConfig", poller_client: "PollerClient"):
        self.session: Optional[ClientSession] = None
        self.key: Optional[str] = None
        self.server: Optional[str] = None
        self.ts: Optional[int] = None
        self.vk_api_config = vk_api_config
        self.is_running = False
        self.poll_task: Optional[asyncio.Task] = None
        self.poller_client = poller_client

    @property
    def params(self):
        return {
            "access_token": self.vk_api_config.access_token,
            "group_id": self.vk_api_config.group_id
        }

    async def start(self):
        print("Poller is starting...")
        self.session = ClientSession()
        await self._get_long_poll_service()
        await self.poller_client.start()
        self.poll_task = asyncio.create_task(self.poll())
        self.is_running = True
        print("Poller started")

    async def stop(self):
        self.is_running = False
        if self.poll_task:
            await self.poll_task
        if self.session:
            await self.session.close()
        await self.poller_client.stop()

    async def _get_long_poll_service(self):
        url: str = build_query(self.vk_api_config.host, method="groups.getLongPollServer",
                               params=self.params)
        async with self.session.get(url) as response:
            json_data = await response.json()
        self.server = json_data["response"]["server"]
        self.key = json_data["response"]["key"]
        self.ts = json_data["response"]["ts"]

    async def poll(self):
        while self.is_running:
            updates = await self.get_updates()
            if updates:
                await self.poller_client.put(updates)

    async def get_updates(self) -> List[Optional[Update]]:
        url = f"{self.server}?act=a_check&key={self.key}&ts={self.ts}&wait=25"
        async with self.session.post(url) as response:
            json_data = await response.json()
            #print(json_data)
        if "failed" in json_data:
            await self._get_long_poll_service()
        else:
            self.ts = json_data.get("ts")
            updates: List[Optional[Update]] = [Update.Schema().load(update) for update in json_data.get("updates", [])]
            return updates
