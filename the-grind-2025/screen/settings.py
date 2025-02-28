import ui
from .title import PreTitle
from .transition import Transition
from .base import Screen
from .smart_text import SmartText
from scenario import haunted_mansion, tutorial, investigation_test


class Settings(SmartText):
    def __init__(self):
        super().__init__(
            text="""The Player
                        chose a(n) {} palette.
                        
                        Player then {} the game.""",
            words=["original", "looked at"],
            known_words={"original", "harsh", "gray", "looked at", "started"}
        )

    def update(self) -> Screen:
        new_state = super().update()

        ui.switch_palette(self.words[0])
        if self.words[1] == "started":
            return PreTitle()
        else:
            return new_state

    def draw(self) -> None:
        super().draw()