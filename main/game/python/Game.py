import pygame
from GameState import GameState
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
        self.pause = False
        self.state = GameState.NOT_RUNNING
        self.fps = fps
        self.clock = pygame.time.Clock() #game clock
    
    def run(self): #main game loop
        self.state = GameState.LAUNCHING
        events = pygame.event.get()
        
        while not self.state == GameState.NOT_RUNNING:
            events = pygame.event.get()
            
            match self.state:
                case GameState.LAUNCHING: #reset all values for game start
                    self.pause = False
                    self.state = GameState.IN_GAME
                case GameState.IN_GAME: #game logic
                    self.state = self.state
                    
                    for event in events:
                        if event.type == pygame.QUIT:
                            self.state = GameState.QUITTING
                case GameState.QUITTING | GameState.NOT_RUNNING: #final actions before closing
                    self.state = GameState.NOT_RUNNING
            self.graphics(self.state)
            self.clock.tick(self.fps)
        pygame.quit()
    
Game("game", 60.0).run()