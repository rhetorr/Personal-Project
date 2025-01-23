import pygame
from GameState import GameState
from util.Clock import StopWatch

# Game about a rocket that gets as far as possible dodging asteroids and collecting fuel
pygame.init()
pygame.font.init()

class Game:
    def __init__(self, fps):
        self.game_running = False
        self.pause = False
        self.state = GameState.NOT_RUNNING
        self.last_state = self.state
        self.fps = fps
        self.clock = pygame.time.Clock()
        
    def get_next_state(self, old_state: GameState):
        match old_state:
            case GameState.NOT_RUNNING:
                self.state = GameState.NOT_RUNNING
            case GameState.LAUNCHING:
                self.state = GameState.IN_GAME
            case GameState.IN_GAME:
                self.state = GameState.QUITTING
            case GameState.QUITTING:
                self.state = GameState.NOT_RUNNING
    def run(self):
        self.game_running = True
        self.pause = False
        self.last_state = self.state
        self.state = GameState.LAUNCHING
        
        while self.game_running:
            
            self.get_next_state(self.state)
            self.last_state = self.state
            
            match self.state:
                case GameState.LAUNCHING:
                    self.state = self.state
                case GameState.QUITTING:
                    self.game_running = False
            
            self.clock.tick(self.fps)
        pygame.quit()
        return self