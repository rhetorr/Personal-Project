from dataclasses import dataclass
import enum

class GameStates(enum.Enum):
    LAUNCHING = 0
    SETTINGS = 1
    MENU = 2
    STARTING = 3
    PLAYING = 4
    LOST = 5
    QUITTING = 6