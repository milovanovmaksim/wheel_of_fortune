import asyncio
from asyncio import Task
from typing import Optional, TYPE_CHECKING
import logging

if TYPE_CHECKING:
    from app.store import Store


logger = logging.getLogger()


class Poller:
    def __init__(self, store: "Store"):
        self.store = store
        self.is_running = False
        self.poll_task: Optional[Task] = None

    async def start(self):
        self.poll_task = asyncio.create_task(self.poll())
        self.is_running = True

    async def stop(self):
        self.is_running = False
        await self.poll_task

    async def poll(self):
        while self.is_running:
            updates = await self.store.vk_api.poll()
            print("updates", updates)
            if updates:
                logger.info(f"New updates: {updates}")
                await self.store.bots_manager.handle_updates(updates)
