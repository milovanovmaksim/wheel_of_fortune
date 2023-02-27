import json

from gui.button import Button


class Menu:

    _buttons = {
        "inline": False,
        "buttons": [
            [
                Button(type_="text",
                       payload="{\"command\":\"game_request\"}",
                       label="Отправить заявку на игру").asdict(),
            ],
            [
                Button(type_="text",
                       payload="{\"command\":\"about\"}",
                       label="Об игре").asdict()
            ]
        ],
        "one_time": False
    }

    @property
    def buttons(self):
        return json.dumps(self._buttons)
