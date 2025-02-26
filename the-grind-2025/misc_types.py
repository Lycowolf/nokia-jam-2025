from enum import Enum, auto

class Way(Enum):
    up = auto(),
    down = auto(),
    left = auto(),
    right = auto(),

    @staticmethod
    def all():
        return [Way.up, Way.down, Way.left, Way.right]
