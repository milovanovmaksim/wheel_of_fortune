import pytest

from bot.state.state import State
from store.quiz.models import AnswerModel


@pytest.fixture
async def question(worker):
    quiz_accessor = worker.state.store.quize_accessor
    theme = await quiz_accessor.create_theme(title="Профессии")
    answer = AnswerModel(title="маляр")
    question = await quiz_accessor.create_question(
        title="Специалист по отделке зданий или помещений.",
        theme_id=theme.id,
        answer=answer
    )
    return question
