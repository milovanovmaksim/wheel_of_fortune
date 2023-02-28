from typing import TYPE_CHECKING, List, Optional
import asyncio

from bot.сhain_responsibility.receivers.receivers import ButtonReceiverAbstract
from bot_long_poll.dcs import Update
from gui.keybord.keyboard import Keyboard
from gui.menu.menu import Menu
from vk_api.dcs import Message


if TYPE_CHECKING:
    from bot.state.state import State
    from store.game.models import GameModel


class StartGameCommandButtonReceiver(ButtonReceiverAbstract):
    def __init__(self, update: Update, state: "State"):
        super().__init__(update, state)

    def set_buttons(self):
        menu = Keyboard()
        buttons = menu.buttons
        self.buttons = buttons

    def set_message(self, **kwargs):
        question = kwargs.get("question")
        lenth = len(question.answer.title)
        answer = "*" * lenth
        self.message = f"Игра началась!! Внимание вопрос.\
            \nТема вопроса: {question.theme.title}\
            \nВопрос: {question.title}\
            \nСлово из {lenth} букв\
            \nСлово: {answer}\
            \nЧтобы назвать все слово отправьте сообщение"

    async def execute(self):
        games: List[Optional["GameModel"]] = await self.game_accessor.get_created_and_started_game_by_player(self.update)
        if games:
            game = games[0]
            if game.state == "Created":
                game.state = "Started"
                game, question = await asyncio.gather(self.game_accessor.update_game_instance(game),
                                                      self.quize_accessor.get_random_question())
                self.set_message(question=question)
                self.set_buttons()
                msg = Message(game.who_next[0], self.message, self.buttons)
                msgs = [Message(vk_api, self.message, "{}") for vk_api in game.who_next[1:]]
                tasks = [self.player_accessor.create_score(game.id, vk_id) for vk_id in game.who_next]
                response = await asyncio.gather(self.send_message(msg),
                                                self.send_messages(msgs),
                                                *tasks,
                                                self.game_accessor.add_question_in_game(game, question))

            elif game.state == "Started":
                lenth = len(game.question.answer.title)
                part1 = f"Тема вопроса: {game.question.theme.title}\
                                \nВопрос: {game.question.title}\
                                \nСлово из {lenth} букв\
                                \nСлово: {game.word}"
                part2 = "\nКоличество зарегистрированых игроков - 1\n"
                part3 = "Игроки:"
                part4 = [f"\n{i+1}. {player.first_name} {player.last_name}" for i, player in enumerate(game.players)]
                all_parts = [part1, part2, part3]
                all_parts.extend(part4[:])
                self.message = " ".join(all_parts)
                self.set_buttons()
                msg = Message(self.update.from_id, self.message, self.buttons)
                response = await self.send_message(msg)
        else:
            self.message = "Зарегистрируйтесь на игру"
            menu = Menu()
            buttons = menu.buttons
            self.buttons = buttons
            msg = Message(self.update.from_id, self.message, self.buttons)
            response = await self.send_message(msg)
        return response

    async def run(self):
        return await self.execute()
