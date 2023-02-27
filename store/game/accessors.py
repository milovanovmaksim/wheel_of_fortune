from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.sql.expression import Select
from sqlalchemy.orm import selectinload, joinedload

from store.game.models import GameModel
from store.quiz.models import QuestionModel

if TYPE_CHECKING:
    from store.database.database import Database
    from bot_long_poll.dcs import Update


@dataclass
class GameAccessor:
    database: "Database"

    async def create_game(self, player=None) -> GameModel:
        if player:
            game_model = GameModel(state="Created",
                                   players=[player],
                                   who_next=[player.vk_id])
        else:
            game_model = GameModel(state="Created",
                                   players=[],
                                   who_next=[])
        async with self.database.session() as session:
            session.add(game_model)
            await session.commit()
            return game_model

    async def _get_one_or_none(self, query: Select) -> Optional[GameModel]:
        async with self.database.session() as session:
            result: Result = await session.execute(query)
            game_model = result.unique().scalar_one_or_none()
            return game_model

    async def get_game_by_state(self, state: str) -> Optional[GameModel]:
        query: Select = (select(GameModel)
                         .options(selectinload(GameModel.players))
                         .where(GameModel.state == state))
        async with self.database.session() as session:
            result: Result = await session.execute(query)
            game_model = result.scalar_one_or_none()
            return game_model

    async def get_game_by_id(self, id: int):
        query: Select = (select(GameModel)
                         .where(GameModel.id == id))
        async with self.database.session() as session:
            result: Result = await session.execute(query)
            game_model = result.scalar_one()
            return game_model

    async def get_started_game_by_player(self, update: "Update") -> Optional[GameModel]:
        query: Select = (select(GameModel)
                         .options(joinedload(GameModel.players))
                         .options(joinedload(GameModel.question)
                                  .joinedload(QuestionModel.answer))
                         .options(joinedload(GameModel.question)
                                  .joinedload(QuestionModel.theme))
                         .where(GameModel.state == "Started")
                         .where(GameModel.who_next.contains([update.from_id])))
        return await self._get_one_or_none(query)

    async def get_created_game_by_player(self, update: "Update") -> Optional[GameModel]:
        query: Select = (select(GameModel)
                         .options(joinedload(GameModel.players))
                         .where(GameModel.state == "Created")
                         .where(GameModel.who_next.contains([update.from_id])))
        return await self._get_one_or_none(query)

    async def get_started_game_id_by_player(self, update: "Update") -> Optional[GameModel]:
        query: Select = (select(GameModel.id)
                         .where(GameModel.state == "Started")
                         .where(GameModel.who_next.contains([update.from_id])))
        return await self._get_one_or_none(query)

    async def get_created_and_started_game_by_player(self, update: "Update"):
        query: Select = (select(GameModel)
                         .options(joinedload(GameModel.players))
                         .options(joinedload(GameModel.question)
                                  .joinedload(QuestionModel.answer))
                         .options(joinedload(GameModel.question)
                                  .joinedload(QuestionModel.theme))
                         .where(GameModel.state.in_(("Created", "Started")))
                         .where(GameModel.who_next.contains([update.from_id])))
        async with self.database.session() as session:
            result: Result = await session.execute(query)
            game_model = result.unique().scalars().all()
            return game_model

    async def add_player_in_game(self, game: GameModel) -> GameModel:
        return await self._update_instance(game)

    async def cancel_game_request(self, game: GameModel) -> GameModel:
        return await self._update_instance(game)

    async def _update_instance(self, game: GameModel) -> GameModel:
        async with self.database.session() as session:
            session.add(game)
            await session.commit()
            return game

    async def quite_game_request(self, game: GameModel) -> GameModel:
        return await self._update_instance(game)

    async def change_game_state_to_started(self, update: "Update") -> Optional[GameModel]:
        game = await self.get_created_game_by_player(update)
        if game:
            game.state = "Started"
            return await self._update_instance(game)

    async def add_question_in_game(self, game: GameModel, question: "QuestionModel") -> GameModel:
        word = "*" * len(question.answer.title)
        game.question = question
        game.question_id = question.id
        game.word = word
        return await self._update_instance(game)

    async def update_game_instance(self, game: "GameModel") -> "GameModel":
        return await self._update_instance(game)
