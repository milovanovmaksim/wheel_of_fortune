import os
import pytest


from bot.state.state import State, setup_state


@pytest.fixture
def state() -> State:
    config_path = os.path.join(
            os.path.abspath(os.path.dirname(__file__)), "..", "config.yml"
        )
    state = setup_state(config_path)
    return state
