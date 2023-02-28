from dataclasses import dataclass, field
from typing import Optional, List, TYPE_CHECKING
import asyncio

from aio_pika import Exchange, IncomingMessage, Queue
from bot.сhain_responsibility.manager import HandlerManager

from broker.broker import Broker
from bot.worker.worker_config import WorkerConfig
from bot_long_poll.dcs import Update


if TYPE_CHECKING:
    from bot.сhain_responsibility.receivers.receivers import R
    from bot.state.state import State


@dataclass
class Worker:
    worker_config: WorkerConfig
    broker: Broker
    handler_manager: HandlerManager
    state: "State"
    exchange: Exchange = field(init=False)
    queue: Queue = field(init=False)
    outbound_queue: Optional[str] = None
    inbound_queue: Optional[str] = None
    tasks: List[asyncio.Task] = field(default_factory=list)

    async def start(self):
        print("Worker is starting...")
        await self._init_broker()
        await self.state.store.connect()
        print("Worker started")

    async def stop(self):
        await self.queue.cancel("_worker")
        await asyncio.gather(*self.tasks, return_exceptions=True)
        await self.state.store.disconnect()
        await self.broker.stop()

    async def _init_broker(self):
        await self.broker.start()
        await self.broker.channel.set_qos(prefetch_count=self.worker_config.capacity)
        self.queue = await self._init_queues()
        await self.queue.consume(self._worker, consumer_tag="_worker")

    async def _init_queues(self):
        return await self.broker.declare_queue(self.outbound_queue)

    async def _worker(self, msg: IncomingMessage):
        async with msg.process():
            task = asyncio.create_task(self.handler(msg))
            self.tasks.append(task)
            await task

    async def handler(self, msg: IncomingMessage):
        body: str = msg.body
        update: Update = Update.Schema().loads(body)
        await self.handle_update(update)

    async def handle_update(self, update: Update):
        receiver: Optional["R"] = self.handler_manager.handle(update, self.state)
        if receiver:
            await receiver.run()
