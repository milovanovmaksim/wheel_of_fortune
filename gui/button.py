from dataclasses import dataclass


@dataclass
class Button:
    type_: str
    label: str
    payload: str = "{}"

    def asdict(self):
        return {
            "action": {
                "type": self.type_,
                "payload": self.payload,
                "label": self.label
            },
        }
