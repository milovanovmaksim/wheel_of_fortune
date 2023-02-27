from dataclasses import field
from typing import List, Optional, Type, ClassVar

from marshmallow_dataclass import dataclass
from marshmallow import Schema, EXCLUDE


from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    BOOLEAN
)
from sqlalchemy.orm import relationship

from app.store.database.sqlalchemy_base import db


@dataclass
class Theme:
    id: Optional[int]
    title: str

    Schema_: ClassVar[Type[Schema]] = Schema

    class Meta:
        unknown = EXCLUDE


@dataclass
class Question:
    id: Optional[int]
    title: str
    theme_id: int
    answers: List["Answer"] = field(default_factory=list)

    Schema_: ClassVar[Type[Schema]] = Schema

    class Meta:
        unknown = EXCLUDE


@dataclass
class Answer:
    title: str
    is_correct: bool

    Schema_: ClassVar[Type[Schema]] = Schema

    class Meta:
        unknown = EXCLUDE


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
    title = Column(String(64), unique=True, index=True, nullable=False)
    theme_id = Column(Integer,  ForeignKey("themes.id", ondelete="CASCADE"), nullable=False, index=True,)
    theme = relationship("ThemeModel", back_populates="questions")
    answers = relationship("AnswerModel", back_populates="question", cascade="all, delete")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "theme_id": self.theme_id,
            "answers": [Answer(**answer.to_dict()) for answer in self.answers]
        }


class AnswerModel(db):
    __tablename__ = "answers"
    id = Column(Integer(), primary_key=True)
    title = Column(String(64), index=True, nullable=False)
    is_correct = Column(BOOLEAN, default=False)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, index=True)
    question = relationship("QuestionModel", back_populates="answers")

    def to_dict(self):
        return {
            "title": self.title,
            "is_correct": self.is_correct,
        }
