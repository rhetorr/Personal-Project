import pygame
from GameStates import GameStates
from util.mathextra.Location import Point
from visuals.Sprite import Sprite
from util.ImageHelpers import ImageHelpers
from util.RectHelpers import RectHelpers
from visuals import VisualsUtil
from visuals.VisualsManager import VisualsManager
from util.TextHelpers import TextHelpers

# Game about a rocket that gets as far as possible dodging asteroids and collecting fuel
pygame.init()
pygame.display.init()
pygame.font.init()

class Game(VisualsManager):
    def __init__(self, caption: str, fps):
        super().__init__((1200,1000), caption, "LOGO.png")
        self.state = GameStates.LAUNCHING
        self.fps = fps
        self.clock = pygame.time.Clock() #game clock
        
    def set_state(self, newState: GameStates) -> GameStates:
        old_state = self.state
        self.state = newState
        return old_state
    
    def run(self): #main game loop
        player = Sprite(self._window_, Point.fill(100), GameStates.PLAYING, GameStates.LOST, GameStates.STARTING).from_image("LOGO.png")
        dt_last_frame = 0.0
        
        self.set_state(GameStates.LAUNCHING)
        while self.state.value.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.set_state(GameStates.NOT_RUNNING)
            
            match self.state:
                case GameStates.LAUNCHING: #reset all values for game start
                    self.set_state(GameStates.MENU)
                case GameStates.SETTINGS | GameStates.MENU | GameStates.STARTING | GameStates.PLAYING | GameStates.LOST: #game logic
                    dt_last_frame = 0
                case GameStates.QUITTING, GameStates.NOT_RUNNING: #final actions before closing
                    self.set_state(GameStates.NOT_RUNNING)
            self.graphics(self.state, player)
            dt_last_frame = self.clock.tick(self.fps) / 1000
        pygame.quit()
    
Game("game", 60.0).run()