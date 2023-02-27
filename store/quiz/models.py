from dataclasses import field, dataclass
from typing import List, Optional


from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    BOOLEAN
)
from sqlalchemy.orm import relationship

from store.database.sqlalchemy_base import db


@dataclass
class Theme:
    id: Optional[int]
    title: str


@dataclass
class Question:
    id: Optional[int]
    title: str
    theme_id: int
    answers: List["Answer"] = field(default_factory=list)


@dataclass
class Answer:
    title: str
    is_correct: bool


class ThemeModel(db):
    __tablename__ = "themes"
    id = Column(Integer, primary_key=True)
    title = Column(String(64), unique=True, index=True, nullable=False)
    questions = relationship("QuestionModel", back_populates="theme", cascade="all, delete")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title
        }


class QuestionModel(db):
    __tablename__ = "questions"
    id = Column(Integer(), primary_key=True)
    title = Column(String(256), unique=True, index=True, nullable=False)
    theme_id = Column(Integer,  ForeignKey("themes.id", ondelete="CASCADE"), nullable=False, index=True,)
    theme = relationship("ThemeModel", back_populates="questions")
    answer = relationship("AnswerModel", back_populates="question", cascade="all, delete", uselist=False)
    games = relationship("GameModel", back_populates="question")


class AnswerModel(db):
    __tablename__ = "answers"
    id = Column(Integer(), primary_key=True)
    title = Column(String(64), index=True, nullable=False)
    is_correct = Column(BOOLEAN, default=False)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, index=True)
    question = relationship("QuestionModel", back_populates="answer", uselist=False)
