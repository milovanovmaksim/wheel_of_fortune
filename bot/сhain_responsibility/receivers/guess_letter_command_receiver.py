import asyncio
from typing import Any, Dict, List, Optional, TYPE_CHECKING
import random

from bot.сhain_responsibility.receivers.mixins import KeyboardMixin, MenuMixins
from bot.сhain_responsibility.receivers.receivers import ButtonReceiverAbstract
from bot_long_poll.dcs import Update
from vk_api.dcs import Message


if TYPE_CHECKING:
    from bot.state.state import State
    from store.quiz.models import QuestionModel
    from store.quiz.models import ThemeModel
    from store.quiz.models import AnswerModel
    from store.game.models import GameModel
    from store.player.models import PlayerModel
    from store.player.models import Score


class GuessLetterCommandButtonReceiver(MenuMixins, KeyboardMixin, ButtonReceiverAbstract):
    def __init__(self, update: Update, state: "State"):
        super().__init__(update, state)
        self.answer: Optional["AnswerModel"] = None
        self.letter: str = ""
        self.result = ""
        self.started_game: Optional["GameModel"] = None
        self.question: Optional["QuestionModel"] = None
        self.score: Optional["Score"] = None
        self.theme: Optional["ThemeModel"] = None
        self.word: List[Optional[str]] = []
        self.correct_answer_score: int = 0

    def set_buttons(self):
        if self.result == self.answer:
            self.buttons = self.get_menu()
        elif self.letter in self.answer.title:
            self.buttons = self.get_keyboard()

    async def execute(self) -> Optional[Dict[str, Any]]:
        self.started_game = await self.game_accessor.get_started_game_by_player(self.update)
        self.score = await self.player_accessor.get_score(self.started_game.id, self.update.from_id)
        self.who_next = self.started_game.who_next
        if self.update.from_id != self.who_next[0]:
            self.message = "Не Ваша очередь"
            return await self.send_message(self.update.from_id)
        self.question: "QuestionModel" = self.started_game.question
        self.theme: "ThemeModel" = self.question.theme
        self.letter: str = self.update.text
        self.answer: "AnswerModel" = self.question.answer
        if self.started_game:
            if self.letter in self.started_game.word:
                await self.send_unsuccessful_message()
            else:
                self.word = [letter for letter in self.started_game.word]
                indexes = self.find_indexes()
                if indexes:
                    self.refresh_result(indexes)
                    if self.result == self.answer.title:
                        await self.stop_game_player_won()
                    else:
                        await self.send_successful_message()
                else:
                    await self.send_unsuccessful_message()
                    await self.game_accessor.update_game_instance(self.started_game)

    async def stop_game_player_won(self):
        self.started_game.state = "Stoped"
        await asyncio.gather(
            self.send_winner_message(),
            self.game_accessor.update_game_instance(self.started_game))

    async def send_successful_message(self):
        self.set_buttons()
        self.correct_answer_score = random.randint(1, 100)
        self.score.score += self.correct_answer_score
        msgs = self.get_successful_messages()
        await asyncio.gather(
            self.player_accessor.update_score_instanse(self.score),
            self.send_messages(msgs),
            self.game_accessor.update_game_instance(self.started_game))

    def refresh_result(self, indexes):
        for index in indexes:
            self.word[index] = self.letter
        self.result = "".join(self.word)
        self.started_game.word = self.result

    def get_player(self, vk_id) -> "PlayerModel":
        for player in self.started_game.players:
            if player.vk_id == vk_id:
                return player

    async def send_winner_message(self):
        player = self.get_player(self.update.from_id)
        text = f"Победу одержал(а): {player.first_name} {player.last_name}\n Ответ: {self.answer.title}"
        msgs = [Message(vk_api, text, self.get_menu()) for vk_api in self.who_next]
        self.started_game.who_next = []
        await self.send_messages(msgs)

    def get_successful_messages(self):
        text = f"Буква {self.letter} в слове присутствует.\
                \nЗа правильный ответ начислено баллов: {self.correct_answer_score}\
                \nВсего баллов: {self.score.score}\
                \nСлово: {self.started_game.word}\
                \nВаш следующий ход."
        player = self.get_player(self.update.from_id)
        text2 = f"Текущий ход у игрока: {player.first_name} {player.last_name}\
                 Игрок назавал букву {self.letter}.\
                 \nСлово: {self.started_game.word}"
        msg = Message(self.update.from_id, text, self.buttons)
        msgs = [Message(vk_id, text2, "{}") for vk_id in self.who_next[1:]]
        msgs.append(msg)
        return msgs

    async def send_unsuccessful_message(self):
        self.change_player_queue()
        next_player_vk_id = self.who_next[0]
        next_player = self.get_player(next_player_vk_id)
        text = f"Неверный ответ. Ход переходит к игроку: \
{next_player.first_name} {next_player.last_name}."
        text2 = f"Ваш ход. \nСлово: {self.started_game.word}"
        msg = Message(self.update.from_id, text, "{}")
        msg2 = Message(self.who_next[0], text2, self.get_keyboard())
        await self.send_messages([msg, msg2])

    def change_player_queue(self):
        current_player = self.who_next.pop(0)
        self.who_next.append(current_player)

    def find_indexes(self):
        indexes = []
        index = self.answer.title.find(self.letter)
        while index >= 0:
            indexes.append(index)
            index = self.answer.title.find(self.letter, index+1)
        return indexes

    async def run(self):
        await self.execute()
