from dataclasses import dataclass
from typing import TYPE_CHECKING


from config import setup_config
from store.store import Store, setup_store


if TYPE_CHECKING:
    from config import Config


@dataclass
class State:
    config: "Config"
    store: Store


def setup_state(path: str) -> State:
    config = setup_config(path)
    store = setup_store(config)
    return State(config, store)
