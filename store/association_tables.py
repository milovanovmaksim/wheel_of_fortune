from store.database.sqlalchemy_base import db


from sqlalchemy import (
    Column,
    ForeignKey,
    Table,
)


palyers_games = Table(
    "association_table",
    db.metadata,
    Column("player_id", ForeignKey("players.id", ondelete="CASCADE"), primary_key=True),
    Column("game_id", ForeignKey("games.id", ondelete="CASCADE"), primary_key=True),
)
