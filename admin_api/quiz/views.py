from typing import TYPE_CHECKING, Optional
from asyncio import gather

from aiohttp_apispec import docs, request_schema, response_schema, querystring_schema
from aiohttp.web_exceptions import HTTPConflict, HTTPNotFound

from app.quiz.models import Answer, Question, Theme
from app.quiz.schemes import (
    ThemeSchema, ResponseThemeSchema, ThemeListResponseSchema,
    QuestionSchema, ResponseQuestionSchema, ListQuestionResponseSchema, ThemeIdSchema
)

from app.web.app import View
from app.web.utils import json_response
from app.web.mixins import AuthRequiredMixin

if TYPE_CHECKING:
    from app.store.quiz.accessor import QuizAccessor


class ThemeAddView(AuthRequiredMixin, View):
    @docs(tags=["quiz"], summary="Add a new theme")
    @request_schema(ThemeSchema)
    @response_schema(ResponseThemeSchema, 200)
    async def post(self):
        title = self.data["title"]
        theme = await self.store.quizzes.get_theme_by_title(title=title)
        if theme:
            raise HTTPConflict(reason=f"Theme with this title ({title}) already exists")
        theme = await self.store.quizzes.create_theme(title=title)
        return json_response(data={"data": theme}, schema=ResponseThemeSchema)


class ThemeListView(AuthRequiredMixin, View):
    @docs(tags=["quiz"], summary="List themes")
    @response_schema(ThemeListResponseSchema, 200)
    async def get(self):
        themes = await self.store.quizzes.list_themes()
        data = {
            "data": {
                "themes": themes
            }
        }
        return json_response(data=data, schema=ThemeListResponseSchema)


class QuestionAddView(AuthRequiredMixin, View):
    @docs(tags=["quiz"], summary="Add a new question")
    @request_schema(QuestionSchema)
    @response_schema(ResponseQuestionSchema, 200)
    async def post(self):
        quiz_accessor: "QuizAccessor" = self.store.quizzes
        results = await self.gather_queries(quiz_accessor)
        self.check_gathered_queries_results(results)
        question = await quiz_accessor.create_question(**self.get_data())
        return json_response(data={"data": question}, schema=ResponseQuestionSchema)

    def get_data(self):
        return {
            "title": self.data["title"],
            "theme_id": self.data["theme_id"],
            "answers": [Answer(**answer) for answer in self.data["answers"]]
        }

    async def gather_queries(self, quiz_accessor: "QuizAccessor") -> tuple[Optional[Theme], Optional[Question]]:
        results = await gather(quiz_accessor.get_theme_by_id(self.data["theme_id"]),
                               quiz_accessor.get_question_by_title(self.data["title"]))
        return results

    def check_gathered_queries_results(self, results: tuple[Optional[Theme], Optional[Question]]):
        theme, question = results
        if theme is None:
            raise HTTPNotFound(reason=f"Theme with id={self.data['theme_id']} is not found")
        if question:
            raise HTTPConflict(reason=f"The question with title <<{(self.data['title'])}>> alredy exists")


class QuestionListView(AuthRequiredMixin, View):
    @docs(tags=["quiz"], summary="List question")
    @querystring_schema(ThemeIdSchema)
    @response_schema(ListQuestionResponseSchema, 200)
    async def get(self):
        theme_id = self.query.get("theme_id")
        quiz_accessor: "QuizAccessor" = self.store.quizzes
        questions = await quiz_accessor.list_questions(theme_id=theme_id)
        data = {
            "data": {
                "questions": questions
            }
        }
        return json_response(data=data, schema=ListQuestionResponseSchema)
