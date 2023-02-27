from abc import ABC, abstractmethod
from typing import List, Optional, Type, TYPE_CHECKING
import asyncio

from bot_long_poll.dcs import Update
from vk_api.dcs import Message
from vk_api.vk_api import VkApi
from .mixins import KeyboardMixin, MenuMixins


if TYPE_CHECKING:
    from bot.state.state import State
    from store.quiz.models import QuestionModel
    from store.quiz.models import AnswerModel
    from store.game.models import GameModel
    from store.player.models import PlayerModel


class Receiver(ABC):
    def __init__(self, update: Update):
        self.update = update

    @abstractmethod
    async def run(self):
        pass


R = Type[Receiver]


class ButtonReceiverAbstract(Receiver):
    def __init__(self, update: Update, state: "State"):
        self.state = state
        self.buttons = "{}"
        self.message: str = ""
        self.player_accessor = self.state.store.player_accessor
        self.game_accessor = self.state.store.game_accessor
        self.quize_accessor = self.state.store.quize_accessor
        super().__init__(update)

    async def send_message(self, message: Message):
        async with VkApi(self.state.config.vk_api_config) as vk:
            response = await vk.send_message(message)
            return response

    async def send_messages(self, messages: List[Message]):
        tasks = [asyncio.create_task(self.send_message(msg)) for msg in messages]
        response = await asyncio.gather(*tasks)
        return response

    async def run(self):
        pass


class StartCommandButtonReceiver(MenuMixins, ButtonReceiverAbstract):
    def __init__(self, update: Update, state: "State"):
        super().__init__(update, state)

    async def create_player(self):
        player_accessor = self.state.store.player_accessor
        player = await player_accessor.get_player_by_vk_id(self.update.from_id)
        if not player:
            player = await player_accessor.create_palyer(self.state, self.update)

    def set_message(self):
        self.message = ("Добро пожаловать в игру Поле Чудес!!\
Вы можете играть в игру один или пригласить друзей.\
Максимальное количество игроков 3.")

    async def run(self):
        self.set_message()
        self.set_buttons()
        await self.create_player()
        msg = Message(self.update.from_id, self.message, self.buttons)
        await self.send_message(msg)


class QuiteCommandButtonReceiver(MenuMixins, ButtonReceiverAbstract):
    def __init__(self, update: Update, state: "State"):
        super().__init__(update, state)

    def set_message(self, **kwargs):
        self.message = "Вы покинули игру"

    async def quite_game(self):

        game = await self.game_accessor.get_started_game_by_player(self.update)
        if game:
            game.who_next.remove(self.update.from_id)
            if not game.who_next:
                game.state = "Stoped"
            await self.game_accessor.quite_game_request(game)

    async def run(self):
        self.set_message()
        self.set_buttons()
        msg = Message(self.update.from_id, self.message, self.buttons)
        await asyncio.gather(self.send_message(msg), self.quite_game())


class CancelGameRequestCommandButtonReceiver(MenuMixins, ButtonReceiverAbstract):
    def __init__(self, update: Update, state: "State"):
        super().__init__(update, state)

    def set_message(self, **kwargs):
        self.message = "Заявка отменена"

    async def cancel_game_request(self):
        game_accessor = self.state.store.game_accessor
        game = await game_accessor.get_created_game_by_player(self.update)
        if game:
            game.who_next.remove(self.update.from_id)
            for player in game.players:
                if player.vk_id == self.update.from_id:
                    game.players.remove(player)
                    break
            await game_accessor.cancel_game_request(game)

    async def run(self):
        self.set_message()
        self.set_buttons()
        msg = Message(self.update.from_id, self.message, self.buttons)
        await asyncio.gather(self.send_message(msg), self.cancel_game_request())


class AboutCommandButtonReceiver(ButtonReceiverAbstract):
    def __init__(self, update: Update, state: "State"):
        super().__init__(update, state)

    def set_message(self, **kwargs):
        self.message = ("Поле Чудес - советская и российская телеигра, \
выходящая каждую пятницу в 19:45 и являющаяся \
частичным аналогом американской телевизионной программы «Колесо Фортуны»")

    async def run(self):
        self.set_message()
        msg = Message(self.update.from_id, self.message, self.buttons)
        return await self.send_message(msg)


class StartTextReceiver(MenuMixins, ButtonReceiverAbstract):
    def __init__(self, update: Update, state: "State"):
        super().__init__(update, state)

    def set_message(self):
        self.message = ("Добро пожаловать в игру Поле Чудес!!\
Вы можете играть в игру один или пригласить друзей.\
Максимальное количество игроков 3.")

    async def run(self):
        self.set_buttons()
        self.set_message()
        msg = Message(self.update.from_id, self.message, self.buttons)
        await self.send_message(msg)


class GuessWordReceiver(MenuMixins, KeyboardMixin, ButtonReceiverAbstract):
    def __init__(self, update: Update, state: "State"):
        super().__init__(update, state)
        self.started_game: Optional["GameModel"] = None
        self.question: Optional["QuestionModel"] = None

    async def execute(self):
        self.started_game = await self.game_accessor.get_started_game_by_player(self.update)
        if self.started_game:
            self.question = self.started_game.question
            self.answer: AnswerModel = self.question.answer
            self.who_next = self.started_game.who_next
            if self.started_game:
                if self.update.from_id != self.who_next[0]:
                    self.message = "Не Ваша очередь"
                    msg = Message(self.update.from_id, self.message, "{}")
                    return await self.send_message(msg)
                text: str = self.update.text.lower()
                if text == self.answer.title:
                    self.refresh_game()
                    await asyncio.gather(self.send_winner_messages(),
                                         self.game_accessor.update_game_instance(self.started_game))
                else:
                    self.delete_player_from_queue()
                    await asyncio.gather(self.send_unsuccessful_message(),
                                         self.game_accessor.update_game_instance(self.started_game))

    def refresh_game(self):
        self.started_game.state = "Stoped"
        self.started_game.who_next = []
        self.started_game.word = self.answer.title

    def get_player(self, vk_id) -> "PlayerModel":
        for player in self.started_game.players:
            if player.vk_id == vk_id:
                return player

    def player_in_queue(self):
        if self.update.from_id != self.who_next[0]:
            self.message = "Не Ваша очередь"

    async def send_winner_messages(self):
        player = self.get_player(self.update.from_id)
        text = f"Победу одержал(а): {player.first_name} {player.last_name}\n Ответ: {self.answer.title}"
        msgs = [Message(vk_api, text, self.get_menu()) for vk_api in self.who_next]
        await self.send_messages(msgs)

    async def send_unsuccessful_message(self):
        if self.who_next:
            text = "Вы неверно назвали слово. Вы выбываете из игры."
            text2 = f"Ваш ход. \nСлово: {self.started_game.word}"
            msg = Message(self.update.from_id, text, "{}")
            msg2 = Message(self.who_next[0], text2, self.get_keyboard())
            await self.send_messages([msg, msg2])
        else:
            text = "Вы неверно назвали слово. Игра окончена."
            msg = Message(self.update.from_id, text, self.get_menu())
            self.started_game.state = "Stoped"
            await self.send_message(msg)

    def delete_player_from_queue(self):
        self.who_next.pop(0)

    async def run(self):
        await self.execute()
