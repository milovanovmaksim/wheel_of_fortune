from typing import Dict, Optional

from aio_pika import Channel, Exchange, ExchangeType, connect, Queue
from aio_pika.abc import AbstractConnection

from broker.config import BrokerConfig


class Broker:
    def __init__(self, config: BrokerConfig):
        self.config = config
        self.queues: Dict[str, Queue] = {}
        self.connection: Optional[AbstractConnection] = None
        self.channel: Optional[Channel] = None

    async def start(self):
        self.connection: AbstractConnection = await connect()
        self.channel: Channel = await self.connection.channel()

    async def declare_queue(self, name: str, **kwargs) -> Queue:
        queue: Queue = await self.channel.declare_queue(name, **kwargs)
        self.queues[queue.name] = queue
        return queue

    async def declare_exchange(self, name: str, type_: ExchangeType, **kwargs):
        exchange: Exchange = await self.channel.declare_exchange(name, type=type_, **kwargs)
        return exchange

    async def stop(self):
        if self.connection:
            await self.connection.close()
        if self.channel:
            await self.channel.close()
