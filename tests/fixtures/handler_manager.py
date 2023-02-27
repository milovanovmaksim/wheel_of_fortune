import pytest
from typing import TYPE_CHECKING

from bot.сhain_responsibility.setup_сhain_responsibility import setup_сhain_responsibility


if TYPE_CHECKING:
    from bot.сhain_responsibility.manager import HandlerManager


@pytest.fixture
def handler_manager() -> "HandlerManager":
    handler_manager = setup_сhain_responsibility()
    return handler_manager
