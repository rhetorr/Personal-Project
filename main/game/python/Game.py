import pygame
from GameState import GameState
from util.RectHelpers import RectHelpers

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
        self.clock = pygame.time.Clock() #game clock
        self.WIN = pygame.display.set_mode((1000,700)) #creating window
        
    def run(self): #main game loop
        self.game_running = True
        self.pause = False
        self.last_state = self.state
        self.state = GameState.LAUNCHING
        
        ra = RectHelpers((600,600)).at(100,100).with_color("white")
        while self.game_running:
            ra = ra.render(self.WIN).with_size(100,100).at(10,10)
            
            self.last_state = self.state
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = GameState.QUITTING
            match self.state:
                case GameState.NOT_RUNNING:
                    self.state = self.state
                case GameState.LAUNCHING:
                    self.state = GameState.IN_GAME
                case GameState.IN_GAME:
                    self.state = self.state
                case GameState.QUITTING:
                    self.game_running = False
                    self.state = GameState.NOT_RUNNING
            
            self.clock.tick(self.fps)
        pygame.quit()
        return self
    
Game(60).run()