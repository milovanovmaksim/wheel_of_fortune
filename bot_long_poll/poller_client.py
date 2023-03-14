from dataclasses import dataclass, field
from typing import Optional

from aio_pika import Exchange, Message

from broker.broker import Broker
from bot_long_poll.dcs import Update


@dataclass
class PollerClient:
    broker: Broker
    exchange: Exchange = field(init=False)
    outbound_queue: Optional[str] = None
    inbound_queue: Optional[str] = None

    async def start(self):
        await self.broker.start()
        await self._init_queues()
        self.exchange = self.broker.channel.default_exchange

    async def stop(self):
        await self.broker.stop()

    async def _init_queues(self):
        await self.broker.declare_queue(self.inbound_queue)

    async def put(self, update: "Update"):
        message = Update.Schema().dumps(update).encode()
        await self.exchange.publish(Message(body=message), routing_key=self.inbound_queue)
