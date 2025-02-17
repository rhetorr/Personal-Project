from dataclasses import dataclass
import enum

@dataclass
class __GameState__:
    _interactable_: bool
    running: bool

class GameStates(enum.Enum):
    NOT_RUNNING = __GameState__(False, False)
    LAUNCHING = __GameState__(False, True)
    SETTINGS = __GameState__(True, True)
    MENU = __GameState__(True, True)
    STARTING = __GameState__(True, True)
    PLAYING = __GameState__(True, True)
    LOST = __GameState__(True, True)
    QUITTING = __GameState__(False, True)