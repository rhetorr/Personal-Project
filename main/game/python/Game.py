import pygame
from GameStates import GameStates
from player.Rocket import Rocket
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
        self.__running__ = False
        
    def set_state(self, newState: GameStates) -> GameStates:
        old_state = self.state
        self.state = newState
        return old_state
    
    def quit_request(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.set_state(GameStates.QUITTING)
        if self.state == GameStates.QUITTING:
            self.__running__ = False
    
    def run(self): #main game loop
        self.__running__ = True
        player = Rocket(self._window_)
        dt_last_frame = 0.0
        
        self.set_state(GameStates.LAUNCHING)
        while self.__running__:
            
            match self.state:
                case GameStates.LAUNCHING: #reset all values for game start
                    self.set_state(GameStates.MENU)
                case GameStates.MENU:
                    if self.play_button.acted_on():
                        self.set_state(GameStates.STARTING)
                    if self.settings_button.acted_on():
                        self.set_state(GameStates.SETTINGS)
                    if self.quit_button.acted_on():
                        self.set_state(GameStates.QUITTING)
                case GameStates.SETTINGS: #settings logic
                    if self.back_button.acted_on():
                        self.set_state(GameStates.MENU)
                case GameStates.STARTING | GameStates.PLAYING | GameStates.LOST: #game logic
                    player.update(self.state)
                case GameStates.QUITTING: #final actions before closings
                    player.at(Point.fill(0)).hide()
            self.graphics(self.state, player)
            dt_last_frame = self.clock.tick(self.fps) / 1000
            self.quit_request()
        pygame.quit()
    
Game("game", 60.0).run()