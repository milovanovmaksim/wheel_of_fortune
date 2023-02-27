import json
from typing import Optional, List, TYPE_CHECKING, Any, Dict


from bot.state.state import State
from bot.сhain_responsibility.receivers.receivers import ButtonReceiverAbstract
from bot_long_poll.dcs import Update
from gui.button import Button
from vk_api.dcs import Message

if TYPE_CHECKING:
    from store.player.models import PlayerModel
    from store.game.models import GameModel


class GameRequestCommandButtonReceiver(ButtonReceiverAbstract):
    def __init__(self, update: Update, state: "State"):
        super().__init__(update, state)

    def set_buttons(self):
        buttons = {
            "inline": False,
            "buttons": [[
                Button("text", "Играть",
                       "{\"command\":\"start_game\"}").asdict(),
                Button("text", "Отменить заявку",
                       "{\"command\":\"cancel_game_request\"}").asdict(),
            ]],
            "one_time": True
        }
        self.buttons = json.dumps(buttons)

    def set_message(self, **kwargs):
        player: Optional["PlayerModel"] = kwargs.get("player")
        players: Optional[List["PlayerModel"]] = kwargs.get("players")
        part = f"{player.first_name} {player.last_name} отправил(а) заявку на игру в Поле Чудес."
        part2 = "\nКоличество зарегистрированых игроков - 1\n"
        part3 = "Игроки:"
        part4 = [f"\n{i+1}. {player.first_name} {player.last_name}" for i, player in enumerate(players)]
        all_parts = [part, part2, part3]
        all_parts.extend(part4[:])
        self.message = " ".join(all_parts)

    async def get_games_by_player(self) -> Optional["GameModel"]:
        games: List[Optional["GameModel"]] = (await self.game_accessor
                                              .get_created_and_started_game_by_player(self.update))
        if games:
            game = games[0]
            if game.state == "Created":
                self.message = "Вы уже зарегистрированы на игру."
            if game.state == "Started":
                lenth = len(game.question.answer.title)
                self.message = f"Вы уже в игре!\n Тема вопроса: {game.question.theme.title}\
                                \nВопрос: {game.question.title}\
                                \nСлово из {lenth} букв\
                                \nСлово: {game.word}"
                buttons = {
                    "inline": False,
                    "buttons": [[
                        Button("text", "Продолжить игру",
                               "{\"command\":\"start_game\"}").asdict(),
                        Button("text", "Выйти из игры", "{\"command\": \"quite\"}").asdict()
                    ]],
                    "one_time": True
                }
                self.buttons = json.dumps(buttons)
            return game
        return None

    async def register_player_to_game(self, player) -> Dict[str, Any]:
        created_game = await self.game_accessor.get_game_by_state("Created")
        if created_game:
            if created_game.players != 3:
                created_game.players.append(player)
                created_game.who_next.append(player.vk_id)
                game = await self.game_accessor.add_player_in_game(created_game)
                self.set_message(player=player, players=game.players)
                msgs = [Message(vk_id, self.message, self.buttons) for vk_id in created_game.who_next]
                return await self.send_messages(msgs)
        created_game = await self.game_accessor.create_game(player=player)
        self.set_message(player=player, players=created_game.players)
        return await self.send_message(Message(player.vk_id, self.message, self.buttons))

    async def execute(self):
        player = await self.player_accessor.get_player_by_vk_id(self.update.from_id)
        if not player:
            player = await self.player_accessor.create_palyer(self.state, self.update)
            return await self.register_player_to_game(player)
        game = await self.get_games_by_player()
        if game:
            return await self.send_message(Message(player.vk_id, self.message, self.buttons))
        response = await self.register_player_to_game(player)
        return response

    async def run(self):
        self.set_buttons()
        await self.execute()
