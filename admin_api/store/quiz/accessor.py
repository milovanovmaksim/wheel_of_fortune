from typing import Optional, List, TypeVar
from dataclasses import asdict

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.sql.expression import Select
from sqlalchemy.orm import joinedload

from app.base.base_accessor import BaseAccessor
from app.quiz.models import (Answer, Theme, Question,
                             ThemeModel, QuestionModel,
                             AnswerModel)


M = TypeVar("M", ThemeModel, QuestionModel)
Obj = TypeVar("Obj", Theme, Question)


class QuizAccessor(BaseAccessor):
    async def create_theme(self, title: str) -> Theme:
        theme_model = ThemeModel(title=title)
        async with self.app.database.session() as session:
            session.add(theme_model)
            await session.commit()
        return Theme(**theme_model.to_dict())

    async def get_theme_by_title(self, title: str) -> Optional[Theme]:
        query: Select = select(ThemeModel).where(ThemeModel.title == title)
        theme = await self._get_one_object(query, Theme)
        return theme

    async def get_theme_by_id(self, id_: int) -> Optional[Theme]:
        query = select(ThemeModel).where(ThemeModel.id == id_)
        theme: Optional[Theme] = await self._get_one_object(query, Theme)
        return theme

    async def _get_one_object(self, query: Select, _object: Obj) -> Optional[Obj]:
        async with self.app.database.session() as session:
            result: Result = await session.execute(query)
        object_model: M = result.unique().scalar_one_or_none()
        if object_model:
            return _object(**object_model.to_dict())
        return None

    async def list_themes(self) -> list[Theme]:
        query: Select = select(ThemeModel)
        async with self.app.database.session() as session:
            result: Result = await session.execute(query)
        themes = [Theme(**theme_model.to_dict()) for theme_model in result.scalars().all()]
        return themes

    async def get_question_by_title(self, title: str) -> Optional[Question]:
        query: Select = (select(QuestionModel)
                         .where(QuestionModel.title == title)
                         .options(joinedload(QuestionModel.answers)))
        question: Optional[Question] = await self._get_one_object(query, Question)
        return question

    async def get_question_by_id(self, _id: int) -> Optional[Question]:
        query: Select = (select(QuestionModel)
                         .where(QuestionModel.id == _id)
                         .options(joinedload(QuestionModel.answers)))
        question: Optional[Question] = await self._get_one_object(query, Question)
        return question

    async def create_question(self, title: str,
                              theme_id: int,
                              answers: List[Answer]) -> Question:
        async with self.app.database.session() as session:
            async with session.begin():
                question_model = QuestionModel(
                    title=title,
                    theme_id=theme_id,
                    answers=[AnswerModel(**asdict(answer)) for answer in answers])
                session.add(question_model)
                await session.commit()
        return Question(**question_model.to_dict())

    async def list_questions(self, theme_id: Optional[int] = None) -> List[Optional[Question]]:
        if theme_id:
            query: Select = (select(QuestionModel)
                             .where(QuestionModel.theme_id == theme_id)
                             .options(joinedload(QuestionModel.answers)))
        else:
            query: Select = (select(QuestionModel)
                             .options(joinedload(QuestionModel.answers)))
        async with self.app.database.session() as session:
            result: Result = await session.execute(query)
        questions_model: List[QuestionModel] = result.unique().scalars().all()
        return [Question(**question_model.to_dict()) for question_model in questions_model]

    async def create_answers(self,
                             question_id: int,
                             answers: list[Answer]) -> list[Answer]:
        async with self.app.database.session() as session:
            async with session.begin():
                query = select(QuestionModel).where(QuestionModel.id == question_id)
                result: Result = await session.execute(query)
                question_model = result.scalar_one()
                answer_models = [
                    AnswerModel(**asdict(answer),
                                question_id=question_id,
                                question=question_model) for answer in answers
                    ]
                session.add_all(answer_models)
                await session.commit()
