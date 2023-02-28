from typing import Any, Optional, List, TYPE_CHECKING
from dataclasses import asdict, dataclass

from sqlalchemy import select
from sqlalchemy.sql.functions import random
from sqlalchemy.engine import Result
from sqlalchemy.sql.expression import Select
from sqlalchemy.orm import joinedload

from store.quiz.models import AnswerModel, QuestionModel, ThemeModel


if TYPE_CHECKING:
    from store.database.database import Database


@dataclass
class QuizAccessor:
    database: "Database"

    async def create_theme(self, title: str) -> ThemeModel:
        theme = ThemeModel(title=title)
        async with self.database.session() as session:
            session.add(theme)
            await session.commit()
        return theme

    async def get_theme_by_title(self, title: str) -> Optional[ThemeModel]:
        query: Select = select(ThemeModel).where(ThemeModel.title == title)
        theme = await self._get_one_object(query, ThemeModel)
        return theme

    async def get_theme_by_id(self, id_: int) -> Optional[ThemeModel]:
        query = select(ThemeModel).where(ThemeModel.id == id_)
        theme: Optional[ThemeModel] = await self._get_one_object(query, ThemeModel)
        return theme

    async def _get_one_object(self, query: Select, object_: Any) -> Optional[Any]:
        async with self.database.session() as session:
            result: Result = await session.execute(query)
        object_ = result.unique().scalar_one_or_none()
        if object_:
            return object_
        return None

    async def list_themes(self) -> list[ThemeModel]:
        query: Select = select(ThemeModel)
        async with self.database.session() as session:
            result: Result = await session.execute(query)
        return result.scalars().all()

    async def get_question_by_title(self, title: str) -> Optional[QuestionModel]:
        query: Select = (select(QuestionModel)
                         .where(QuestionModel.title == title)
                         .options(joinedload(QuestionModel.answer)))
        question: Optional[QuestionModel] = await self._get_one_object(query, QuestionModel)
        return question

    async def get_question_by_id(self, _id: int) -> Optional[QuestionModel]:
        query: Select = (select(QuestionModel)
                         .where(QuestionModel.id == _id)
                         .options(joinedload(QuestionModel.answer)))
        question: Optional[QuestionModel] = await self._get_one_object(query, QuestionModel)
        return question

    async def create_question(self, title: str,
                              theme_id: int,
                              answer: AnswerModel) -> QuestionModel:
        async with self.database.session() as session:
            async with session.begin():
                question_model = QuestionModel(
                    title=title,
                    theme_id=theme_id,
                    answer=answer)
                session.add(question_model)
                await session.commit()
        return question_model

    async def list_questions(self, theme_id: Optional[int] = None) -> List[Optional[QuestionModel]]:
        if theme_id:
            query: Select = (select(QuestionModel)
                             .where(QuestionModel.theme_id == theme_id)
                             .options(joinedload(QuestionModel.answer))
                             .options(joinedload(QuestionModel.theme)))
        else:
            query: Select = (select(QuestionModel)
                             .options(joinedload(QuestionModel.answer))
                             .options(joinedload(QuestionModel.theme)))
        async with self.database.session() as session:
            result: Result = await session.execute(query)
        questions_model: List[QuestionModel] = result.unique().scalars().all()
        return questions_model

    async def create_answers(self,
                             question_id: int,
                             answers: list[AnswerModel]) -> list[AnswerModel]:
        async with self.database.session() as session:
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
                return answer_models

    async def get_random_question(self) -> Optional[QuestionModel]:
        query = (select(QuestionModel)
                 .options(joinedload(QuestionModel.answer))
                 .options(joinedload(QuestionModel.theme))
                 .order_by(random()).limit(1))
        async with self.database.session() as session:
            result: Result = await session.execute(query)
            question = result.unique().scalar_one_or_none()
            return question
