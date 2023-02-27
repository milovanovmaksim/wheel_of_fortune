import json
from dataclasses import dataclass

from gui.button import Button


@dataclass
class Keyboard:
    _buttons = {
        "inline": False,
        "buttons": [
            [Button("text", "Выйти из игры", "{\"command\": \"quite\"}").asdict()],
            [Button("text", letter, json.dumps({"command": "guess_letter", "letter": letter})).asdict() for letter in "йцуке"],
            [Button("text", letter, json.dumps({"command": "guess_letter", "letter": letter})).asdict() for letter in "нгшщз"],
            [Button("text", letter, json.dumps({"command": "guess_letter", "letter": letter})).asdict() for letter in "хъфыв"],
            [Button("text", letter, json.dumps({"command": "guess_letter", "letter": letter})).asdict() for letter in "апрол"],
            [Button("text", letter, json.dumps({"command": "guess_letter", "letter": letter})).asdict() for letter in "джэяч"],
            [Button("text", letter, json.dumps({"command": "guess_letter", "letter": letter})).asdict() for letter in "смить"],
            [Button("text", letter, json.dumps({"command": "guess_letter", "letter": letter})).asdict() for letter in "бю"],
            ],
        "one_time": True
    }

    @property
    def buttons(self):
        return json.dumps(self._buttons)
