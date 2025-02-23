from typing import Self

class Screen:
    # Screens form a state machine. update() method updates self as necessary and returns a Screen to be displayed
    # (which can be self).
    def update(self) -> Self:
        pass

    def draw(self):
        pass