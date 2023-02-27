from dataclasses import field, dataclass
from typing import List, TYPE_CHECKING, Literal

from sqlalchemy import (
    CheckConstraint,
    Column,
    Integer,
    String,
    ForeignKey

)

from sqlalchemy.orm import relationship
from store.database.sqlalchemy_base import db
from store.association_tables import palyers_games
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.mutable import MutableList

if TYPE_CHECKING:
    from store.player.models import Player


@dataclass
class Game:
    id_: int
    srate: Literal["Created", "Started", "Stoped"]
    queue_players: List["Player"] = field(default_factory=list)


class GameModel(db):
    __tablename__ = "games"
    id = Column(Integer, primary_key=True)
    state = Column(String(64), index=True, nullable=False)
    players = relationship("PlayerModel", secondary=palyers_games, back_populates="games")
    who_next = Column(MutableList.as_mutable(ARRAY(Integer, dimensions=1)))
    question_id = Column(Integer,  ForeignKey("questions.id"), index=True)
    question = relationship("QuestionModel", back_populates="games")
    word = Column(String(64))

    __table_args__ = (
        CheckConstraint(
                ("((state)::text = ANY (ARRAY[('Created'::character varying)::text, \
                    ('Started'::character varying)::text, ('Stoped'::character varying)::text]))"),
                name="games_state_check"),)
