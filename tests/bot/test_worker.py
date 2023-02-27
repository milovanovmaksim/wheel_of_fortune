import asyncio
import random
from unittest.mock import AsyncMock, Mock
from bot.state.state import State

from bot.worker.worker import Worker
from bot_long_poll.dcs import Update
from store.game.models import GameModel
from store.player.models import Score
from vk_api.dcs import Message
from vk_api.vk_api import VkApi
from .data import (COMMANDS_USER1, COMMANDS_USER2, user1, about_response_message,
                   start_command_response_message,
                   game_request_response_message,
                   start_game_response_message,
                   guess_letter_correct_response_message,
                   guess_letter_incorrect_response_message,
                   guess_word_correct_response_message,
                   guess_word_incorrect_response_message)


class TestWorker:
    async def test_start_command(self, worker: Worker, state: State):
        update: Update = COMMANDS_USER1["start"]
        VkApi.send_message = AsyncMock(return_value=start_command_response_message)
        VkApi.get_user = AsyncMock(return_value=user1)
        await worker.handle_update(update)
        player_accessor = state.store.player_accessor
        user = await player_accessor.get_player_by_vk_id(update.from_id)
        assert user.first_name == user1.first_name
        assert user.last_name == user1.last_name
        assert user.vk_id == update.from_id
        assert user.id == 1

    async def test_about_command(self, worker: Worker, state: State):
        update: Update = COMMANDS_USER1["about"]
        VkApi.send_message = AsyncMock(return_value=about_response_message)
        await worker.handle_update(update)
        assert VkApi.send_message.call_count == 1
        message: Message = VkApi.send_message.mock_calls[0].args[0]
        assert message.user_id == update.from_id

    async def test_game_request(sekf, worker: Worker, state: State):
        update: Update = COMMANDS_USER1["game_request"]
        VkApi.send_message = AsyncMock(return_value=game_request_response_message)
        VkApi.get_user = AsyncMock(return_value=user1)
        await worker.handle_update(update)
        game_accessor = state.store.game_accessor
        game = await game_accessor.get_created_game_by_player(update)
        assert update.from_id in game.who_next
        assert game.state == "Created"
        assert len(game.players) == 1
        assert user1.first_name == game.players[0].first_name

    async def test_start_game_command(self, worker: Worker,
                                      state: State, player_1, question):
        update: Update = COMMANDS_USER1["start_game"]
        VkApi.send_message = AsyncMock(return_value=start_game_response_message)
        await worker.handle_update(update)
        game_accessor = state.store.game_accessor
        started_game = await game_accessor.get_started_game_by_player(update)
        assert update.from_id in started_game.who_next
        assert started_game.state == "Started"
        assert len(started_game.players) == 1
        assert started_game.question.title == question.title

    async def test_guess_letter_correct_answer(self, worker: Worker, state: State,
                                               question, player_1, started_game):
        update: Update = COMMANDS_USER1["guess_letter_correct"]
        game_accessor = state.store.game_accessor
        player_accessor = state.store.player_accessor
        VkApi.send_message = AsyncMock(return_value=guess_letter_correct_response_message)
        random.randint = Mock(return_value=14)
        score_before: Score = await player_accessor.get_score(started_game.id, update.from_id)
        await worker.handle_update(update)
        game: GameModel = await game_accessor.get_started_game_by_player(update)
        score_after: Score = await player_accessor.get_score(game.id, update.from_id)
        assert game.word == "м****"
        assert update.text in question.answer.title  # провепяем, что есть такая буква
        assert game.who_next[0] == player_1.vk_id  # т.к ответ верный ход остается у текущего игрока
        assert score_after.score - score_before.score == 14  # проверяем, что за правильный ответ начислено 14 баллов

    async def test_guess_letter_incorrect_answer(self, worker: Worker,
                                                 state: State, question, player_1,
                                                 player_2, started_game):
        update_user1: Update = COMMANDS_USER1["guess_letter_incorrect"]
        VkApi.send_message = AsyncMock(return_value=guess_letter_incorrect_response_message)
        await worker.handle_update(update_user1)
        game_accessor = state.store.game_accessor
        game: GameModel = await game_accessor.get_started_game_by_player(update_user1)
        assert update_user1.text not in question.answer.title  # провепяем, что нет такой буква
        assert game.word == "*****"
        assert game.who_next[1] == player_1.vk_id  # т.к ответет не верный игрок(player_1) перемещается в конец очереди
        assert game.who_next[0] == player_2.vk_id  # ход перешел к следующему игроку (player_2)

    async def test_guess_word_correct_answer(self, worker: Worker,
                                             state: State, question, player_1,
                                             player_2, started_game):

        update_user1: Update = COMMANDS_USER1["guess_word_correct"]
        game_accessor = state.store.game_accessor
        started_game.state == "Started"
        VkApi.send_message = AsyncMock(return_value=guess_word_correct_response_message)
        await worker.handle_update(update_user1)
        game: GameModel = await game_accessor.get_game_by_id(started_game.id)
        assert game.state == "Stoped"  # Игра остановлена, есть победитель
        assert len(game.who_next) == 0
        assert update_user1.text == question.answer.title  # Проверяем, что слово верно

    async def test_guess_word_incorrect_answer(self, worker: Worker,
                                               state: State, question, player_1,
                                               player_2, started_game):

        update_user1: Update = COMMANDS_USER1["guess_word_incorrect"]
        game_accessor = state.store.game_accessor
        started_game.state == "Started"
        VkApi.send_message = AsyncMock(return_value=guess_word_incorrect_response_message)
        await worker.handle_update(update_user1)
        game: GameModel = await game_accessor.get_game_by_id(started_game.id)
        assert game.state == "Started"
        assert player_1.vk_id not in game.who_next  # слово названо неверно, игрок удаляется из игры
        assert game.who_next[0] == player_2.vk_id  # ход переходит к следующему игроку
        assert update_user1.text != question.answer.title

    async def test_restart_worker(self, worker: Worker,
                                  state: State, question, player_1,
                                  player_2, started_game):
        update_user1: Update = COMMANDS_USER1["guess_letter_incorrect"]
        VkApi.send_message = AsyncMock(return_value=guess_letter_incorrect_response_message)
        who_next_before_restart = started_game.who_next
        # Игрок назавал неправильную букву. Должен произойти переход хода к следующему игроку.
        # В этот же самый момент отключаем сервис и запускаем заново. Бот должен пережить рестарт и завершить таски,
        # сохранив состояние игры. Игрок, назвавший неверную букву должен оказаться в конце очереди.
        await asyncio.gather(
            worker.stop(),
            worker.handle_update(update_user1)
        )
        await worker.start()

        game_accessor = state.store.game_accessor
        game: GameModel = await game_accessor.get_game_by_id(started_game.id)
        who_next_after_restart = game.who_next

        # проверяем, что бот пережил рестарт и завершил все таски корректно, т.е игрок должен оказаться в конце очереди.
        assert who_next_before_restart[0] == who_next_after_restart[-1]
