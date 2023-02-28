import logging
from unittest.mock import AsyncMock
import pytest
from typing import TYPE_CHECKING

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from bot.state.state import State
from store.game.models import GameModel

from tests.bot.data import (COMMANDS_USER1, COMMANDS_USER2, user1,
                            game_request_response_message, start_game_response_message)
from vk_api.vk_api import VkApi

if TYPE_CHECKING:
    from bot.worker.worker import Worker
    from bot_long_poll.dcs import Update


@pytest.fixture(autouse=True, scope="function")
async def clear_db(worker: "Worker", stop_worker):
    yield
    try:
        session = AsyncSession(worker.state.store.database._engine)
        connection = await session.connection()
        for table in worker.state.store.database._db.metadata.sorted_tables:
            if table.name != "association_table":
                await session.execute(text(f"TRUNCATE {table.name} CASCADE"))
                await session.execute(text(f"ALTER SEQUENCE {table.name}_id_seq RESTART WITH 1"))

        await session.commit()
        await connection.close()
    except Exception as err:
        logging.warning(err)


@pytest.fixture
async def player_1(worker: "Worker", state: State):
    update: "Update" = COMMANDS_USER1["game_request"]
    VkApi.get_user = AsyncMock(return_value=user1)
    VkApi.send_message = AsyncMock(return_value=game_request_response_message)
    await worker.handle_update(update)
    player_accessor = state.store.player_accessor
    player = await player_accessor.get_player_by_vk_id(update.from_id)
    return player


@pytest.fixture
async def player_2(worker: "Worker", state: State):
    update: "Update" = COMMANDS_USER2["game_request"]
    VkApi.get_user = AsyncMock(return_value=user1)
    VkApi.send_message = AsyncMock(return_value=game_request_response_message)
    await worker.handle_update(update)
    player_accessor = state.store.player_accessor
    player = await player_accessor.get_player_by_vk_id(update.from_id)
    return player


@pytest.fixture
async def started_game(worker: "Worker", state: State):
    update: "Update" = COMMANDS_USER1["start_game"]
    VkApi.send_message = AsyncMock(return_value=start_game_response_message)
    await worker.handle_update(update)
    game_accessor = state.store.game_accessor
    game: GameModel = await game_accessor.get_started_game_by_player(update)
    return game
