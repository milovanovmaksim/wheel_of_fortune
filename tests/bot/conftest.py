import pytest
from typing import TYPE_CHECKING

from bot.сhain_responsibility.setup_сhain_responsibility import setup_сhain_responsibility
from bot.worker.worker import Worker
from bot.worker.worker_config import WorkerConfig


if TYPE_CHECKING:
    from bot.state.state import State
    from broker.broker import Broker


@pytest.fixture
def worker(state: "State",
           broker: "Broker") -> Worker:
    worker_config = WorkerConfig()
    handler_manager = setup_сhain_responsibility()
    return Worker(state=state,
                  handler_manager=handler_manager,
                  worker_config=worker_config,
                  broker=broker)


@pytest.fixture(autouse=True)
async def start_worker(worker: Worker):
    await worker.start()


@pytest.fixture
async def stop_worker(worker: Worker):
    yield
    await worker.stop()

