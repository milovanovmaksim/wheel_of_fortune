from typing import Dict, Optional

from aio_pika import Channel, Exchange, ExchangeType, connect, Queue
from aio_pika.abc import AbstractConnection, AbstractChannel, AbstractQueue

from broker.config import BrokerConfig


class Broker:
    def __init__(self, config: BrokerConfig):
        self.config = config
        self.queues: Dict[str, AbstractQueue] = {}
        self.connection: Optional[AbstractConnection] = None
        self.channel: Optional[AbstractChannel] = None

    async def start(self):
        self.connection: Optional[AbstractConnection] = await connect()
        if self.connection:
            self.channel: Optional[AbstractChannel] = await self.connection.channel()

    async def declare_queue(self, name: str, **kwargs) -> Optional[AbstractQueue]:
        if self.channel:
            queue: AbstractQueue = await self.channel.declare_queue(name, **kwargs)
            self.queues[queue.name] = queue
            return queue

    async def declare_exchange(self, name: str, type_: ExchangeType, **kwargs) -> Optional[Exchange]:
        if self.channel:
            exchange: Exchange = await self.channel.declare_exchange(name, type=type_, **kwargs)
            return exchange

    async def stop(self):
        if self.connection:
            await self.connection.close()
        if self.channel:
            await self.channel.close()
