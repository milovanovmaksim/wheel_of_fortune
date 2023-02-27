import typing
import asyncio

from app.store.vk_api.dataclasses import Update, Message

if typing.TYPE_CHECKING:
    from app.web.app import Application


class BotManager:
    def __init__(self, app: "Application"):
        self.app = app

    async def handle_updates(self, updates: list[Update]):
        tasks = []
        for update in updates:
            user_id = update.object.user_id
            text = "From vk-bot"
            message = Message(user_id, text)
            task = asyncio.create_task(self.app.store.vk_api.send_message(message))
            tasks.append(task)
        await asyncio.gather(*tasks)
