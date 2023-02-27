import asyncio
from typing import TYPE_CHECKING

from bot.worker.worker import Worker
from bot.worker.worker_config import WorkerConfig
from bot.сhain_responsibility.manager import HandlerManager
from bot.state.state import setup_state
from broker.broker import Broker
from bot.сhain_responsibility.setup_сhain_responsibility import setup_сhain_responsibility


if TYPE_CHECKING:
    from bot.state.state import State


def run_bot_worker():
    state: "State" = setup_state("./config.yml")
    handler_manager: HandlerManager = setup_сhain_responsibility()
    worker_config = WorkerConfig()
    broker = Broker(state.config.broker_config)
    bot_worker = Worker(broker=broker, worker_config=worker_config,
                        outbound_queue="updates", handler_manager=handler_manager,
                        state=state)

    loop = asyncio.get_event_loop()
    try:
        loop.create_task(bot_worker.start())
        loop.run_forever()
    except KeyboardInterrupt:
        print("\nBotWorker is shutting down ...")
        loop.run_until_complete(bot_worker.stop())
        print("BotWorker shutted down")


if __name__ == "__main__":
    run_bot_worker()
