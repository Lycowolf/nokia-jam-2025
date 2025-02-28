from ui import draw_wrapped_text, draw_text_row
from input import btnp as pressed, Map
from .smart_text import SmartText

class ItemScreen(SmartText):
    def __init__(self, prev_screen, text):
        super().__init__(text, [], [])
        self.prev = prev_screen
        self.text = text

    def draw(self):
        super().draw()

        if self.is_bottom():
            draw_text_row(6, "...", x_off=-3)

    def update(self):
        new_state = super().update()
        if new_state != self:
            return new_state

        if pressed(Map.action) or pressed(Map.back):
            return self.prev
        else:
            return self
