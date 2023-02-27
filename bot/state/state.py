from dataclasses import dataclass
from typing import TYPE_CHECKING


from config import setup_config
from store.database.database import Database
from store.store import Store, setup_store


if TYPE_CHECKING:
    from config import Config


@dataclass
class State:
    config: "Config"
    database: Database
    store: Store

    async def init(self):
        await self.database.connect()


def setup_state(path: str) -> State:
    config = setup_config(path)
    database = Database(config)
    store = setup_store(database)
    return State(config, database, store)
