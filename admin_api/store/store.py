import typing

from store.admin.accessor import AdminAccessor
from store.database.database import Database
from store.game.accessors import GameAccessor
from store.player.accessors import PlayerAccessors
from store.quiz.accessor import QuizAccessor
from store.store import Store


if typing.TYPE_CHECKING:
    from admin_api.web.app import Application


def setup_store(app: "Application"):
    app.database = Database(app.config)
    player_accessor = PlayerAccessors(app.database)
    game_accessor = GameAccessor(app.database)
    quize_accessor = QuizAccessor(app.database)
    admin_accessor = AdminAccessor(app.database)
    app.store = Store(player_accessor, game_accessor,
                      quize_accessor, admin_accessor, app.database)
    app.on_startup.append(app.store.connect)
    app.on_cleanup.append(app.store.disconnect)
