import os
import pytest

from broker.broker import Broker
from broker.config import setup_config


@pytest.fixture
def broker() -> Broker:
    config_path = os.path.join(
            os.path.abspath(os.path.dirname(__file__)), "..", "config.yml"
        )
    broker_config = setup_config(config_path)
    return Broker(broker_config)
