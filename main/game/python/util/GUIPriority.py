from enum import Enum

class GUIPriority(Enum):
    BACKGROUND = 0
    SCREEN = 1
    MENU_GUI = 2
    SPRITE = 3
    GAME_GUI = 4
    PAUSE_GUI = 5
    OVERLAY = 6