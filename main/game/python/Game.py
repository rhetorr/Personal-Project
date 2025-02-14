import pygame
from GameState import GameState
from util.GUIPriority import GUIPriority
from visuals.Sprite import Sprite
from util.ImageHelpers import ImageHelpers
from util.RectHelpers import RectHelpers
from visuals import VisualsUtil
from visuals.VisualsManager import VisualsManager

# Game about a rocket that gets as far as possible dodging asteroids and collecting fuel
pygame.init()
pygame.display.init()
pygame.font.init()

class Game(VisualsManager):
    def __init__(self, caption: str, fps):
        super().__init__((1200,1000), caption, "LOGO.png")
        self.state = GameState.NOT_RUNNING
        self.fps = fps
        self.clock = pygame.time.Clock() #game clock
    
    def run(self): #main game loop
        self.state = GameState.LAUNCHING
        player = Sprite((500, 500), GUIPriority.SPRITE).from_image("LOGO.png")
        
        while not self.state == GameState.NOT_RUNNING:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = GameState.QUITTING
            
            match self.state:
                case GameState.LAUNCHING: #reset all values for game start
                    self.state = GameState.IN_GAME
                case GameState.IN_GAME: #game logic
                    self.state = self.state
                case GameState.QUITTING | GameState.NOT_RUNNING: #final actions before closing
                    self.state = GameState.NOT_RUNNING
            self.graphics(self.state, [player])
            self.clock.tick(self.fps)
        pygame.quit()
    
Game("game", 60.0).run()