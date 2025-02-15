from dataclasses import dataclass
import enum

class GameState(enum.Enum):
    NOT_RUNNING = 0
    LAUNCHING = 1
    IN_GAME = 2
    QUITTING = 999
    
class PlayState(enum.Enum):
    OUT_OF_BOUNDS = 0
    MENU = 1
    STARTING = 2
    PLAYING = 3
    LOST = 4
    PAUSED = 5
    
class MenuPages(enum.Enum):
    OUT_OF_BOUNDS = 0
    TITLE_PAGE = 1
    SETTINGS = 2

@dataclass
class FullState:
    game_state: GameState
    play_state: PlayState
    menu_page: MenuPages
    
def in_game():
    return FullState(GameState.IN_GAME, PlayState.PLAYING, MenuPages.OUT_OF_BOUNDS)