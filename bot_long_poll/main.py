import asyncio
from typing import TYPE_CHECKING


from bot_long_poll.poller_client import PollerClient
from broker.broker import Broker
from bot_long_poll.poller import Poller
from config import setup_config

if TYPE_CHECKING:
    from config import Config


def run_poller():
    config: "Config" = setup_config("./config.yml")
    broker = Broker(config.broker_config)
    poller_client = PollerClient(broker, inbound_queue="updates")
    poller = Poller(vk_api_config=config.vk_api_config, poller_client=poller_client)

    loop = asyncio.get_event_loop()
    try:
        loop.create_task(poller.start())
        loop.run_forever()
    except KeyboardInterrupt:
        print("\nPoller is shutting down ...")
        loop.run_until_complete(poller.stop())
        print("Poller shutted down")


if __name__ == "__main__":
    run_poller()
