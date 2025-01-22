import enum

class GameState(enum.Enum):
    NOT_RUNNING = 0
    LAUNCHING = 1
    IN_GAME = 2
    QUITTING = 999