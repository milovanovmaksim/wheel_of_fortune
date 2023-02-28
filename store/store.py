from dataclasses import dataclass
from config import Config

from store.admin.accessor import AdminAccessor
from store.player.accessors import PlayerAccessors
from store.game.accessors import GameAccessor
from store.quiz.accessor import QuizAccessor
from store.database.database import Database


@dataclass
class Store:
    player_accessor: PlayerAccessors
    game_accessor: GameAccessor
    quize_accessor: QuizAccessor
    admin_accessor: AdminAccessor
    database: Database

    async def connect(self, *_: list, **__: dict):
        await self.database.connect()

    async def disconnect(self,  *_: list, **__: dict):
        await self.database.disconnect()


def setup_store(config: "Config"):
    database = Database(config)
    player_accessor = PlayerAccessors(database)
    game_accessor = GameAccessor(database)
    quize_accessor = QuizAccessor(database)
    admin_accessor = AdminAccessor(database)
    return Store(player_accessor, game_accessor,
                 quize_accessor, admin_accessor, database)
