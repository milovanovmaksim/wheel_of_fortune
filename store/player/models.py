from dataclasses import field, dataclass
from typing import List, TYPE_CHECKING

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)
from sqlalchemy.orm import relationship

from store.database.sqlalchemy_base import db
from store.association_tables import palyers_games

if TYPE_CHECKING:
    from store.game.models import Game


@dataclass
class Player:
    id_: int
    vk_id: int
    first_name: str
    last_name: str
    game_id: int
    games: List["Game"] = field(default_factory=list)


class PlayerModel(db):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True)
    vk_id = Column(Integer, unique=True, index=True, nullable=False)
    first_name = Column(String(64), index=True, nullable=False)
    last_name = Column(String(64), index=True, nullable=False)
    games = relationship("GameModel", secondary=palyers_games, back_populates="players")


class Score(db):
    __tablename__ = "scores"
    id = Column(Integer, primary_key=True)
    score = Column(Integer, default=0)
    player_vk_id = Column(Integer,  ForeignKey("players.vk_id"), index=True)
    game_id = Column(Integer,  ForeignKey("games.id"), index=True)
