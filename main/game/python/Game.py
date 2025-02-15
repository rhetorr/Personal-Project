import pygame
from GameStates import FullState, GameState, MenuPages, PlayState, in_game
from util.mathextra.Location import Point
from util.GUIPriority import GUIPriority
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
        self.state = FullState(GameState.NOT_RUNNING, PlayState.OUT_OF_BOUNDS, MenuPages.OUT_OF_BOUNDS)
        self.fps = fps
        self.clock = pygame.time.Clock() #game clock
    
    def run(self): #main game loop
        self.state = FullState(GameState.LAUNCHING, PlayState.OUT_OF_BOUNDS, MenuPages.OUT_OF_BOUNDS)
        player = Sprite(Point.fill(100), GUIPriority.SPRITE, in_game()).from_image("LOGO.png")
        dt_last_frame = 0.0
        
        while not self.state.game_state == GameState.NOT_RUNNING:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state.game_state = GameState.QUITTING
            
            match self.state.game_state:
                case GameState.LAUNCHING: #reset all values for game start
                    self.state.game_state = GameState.IN_GAME
                case GameState.IN_GAME: #game logic
                    self.state = self.state
                case GameState.QUITTING | GameState.NOT_RUNNING: #final actions before closing
                    self.state.game_state = GameState.NOT_RUNNING
            self.graphics(self.state, [player])
            dt_last_frame = self.clock.tick(self.fps) / 1000
        pygame.quit()
    
Game("game", 60.0).run()