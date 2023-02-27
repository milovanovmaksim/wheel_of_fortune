from typing import TYPE_CHECKING
from dataclasses import dataclass

from store.player.accessors import PlayerAccessors
from store.game.accessors import GameAccessor
from store.quiz.accessor import QuizAccessor


if TYPE_CHECKING:
    from store.database.database import Database


@dataclass
class Store:
    player_accessor: PlayerAccessors
    game_accessor: GameAccessor
    quize_accessor: QuizAccessor


def setup_store(database: "Database"):
    player_accessor = PlayerAccessors(database)
    game_accessor = GameAccessor(database)
    quize_accessor = QuizAccessor(database)
    return Store(player_accessor, game_accessor, quize_accessor)
