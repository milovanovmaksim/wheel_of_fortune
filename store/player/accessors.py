from typing import TYPE_CHECKING, Optional
from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.sql.expression import Select
from sqlalchemy.orm import selectinload
from store.player.models import PlayerModel, Score
from vk_api.vk_api import VkApi

if TYPE_CHECKING:
    from bot_long_poll.dcs import Update
    from bot.state.state import State
    from vk_api.dcs import User
    from store.database.database import Database



@dataclass
class PlayerAccessors:
    database: "Database"

    async def create_palyer(self, state: "State", update: "Update") -> Optional[PlayerModel]:
        user: Optional["User"] = await self.get_user(state, update)
        player_model: Optional[PlayerModel] = None
        if user:
            async with self.database.session() as session:
                player_model = PlayerModel(vk_id=update.from_id,
                                           first_name=user.first_name,
                                           last_name=user.last_name,)
                session.add(player_model)
                await session.commit()
        return player_model

    async def get_user(self, state: "State", update: "Update") -> Optional["User"]:
        async with VkApi(state.config.vk_api_config) as vk:
            user = await vk.get_user(update.from_id)
            print(user)
            return user

    async def get_player_by_vk_id(self, from_id: int) -> PlayerModel:
        query: Select = (select(PlayerModel)
                         .options(selectinload(PlayerModel.games))
                         .where(PlayerModel.vk_id == from_id))
        async with self.database.session() as session:
            result: Result = await session.execute(query)
            player_model = result.scalar_one_or_none()
            return player_model

    async def create_score(self, game_id: int, player_vk_id: int) -> Score:
        async with self.database.session() as session:
            score = Score(game_id=game_id, player_vk_id=player_vk_id)
            session.add(score)
            await session.commit()
            return score

    async def get_score(self, game_id: int, vk_id: int) -> Score:
        query: Select = (select(Score)
                         .where(Score.game_id == game_id)
                         .where(Score.player_vk_id == vk_id))
        async with self.database.session() as session:
            result: Result = await session.execute(query)
            score = result.scalar_one_or_none()
            return score

    async def update_score_instanse(self, score: Score) -> Score:
        async with self.database.session() as session:
            session.add(score)
            await session.commit()
            return score
