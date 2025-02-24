from abc import ABC
from typing import Self

class Screen(ABC):
    # Screens form a state machine. update() method updates self as necessary and returns a Screen to be displayed
    # (which can be self).
    def update(self) -> Self:
        pass

    def draw(self):
        pass