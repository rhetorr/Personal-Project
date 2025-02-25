import time
import threading
import pygame
from GameStates import GameStates
from util.MouseUtil import Mouse, ClickType
from player.Rocket import Rocket
from util.mathextra.Location import Point
from visuals.Sprite import Sprite
from util.ImageHelpers import ImageHelpers
from util.RectHelpers import RectHelpers
from visuals import VisualsUtil
from visuals.VisualsManager import VisualsManager
from util.TextHelpers import TextHelpers
import Settings

# Game about a rocket that gets as far as possible dodging asteroids and collecting fuel
pygame.init()
pygame.display.init()
pygame.font.init()

class Game(VisualsManager):
    def __init__(self, caption: str, fps: int):
        super().__init__((1200,1000), caption, "LOGO.png", Mouse())
        self.state = GameStates.LAUNCHING
        self.fps = fps
        self.clock = pygame.time.Clock() #game clock
        self.__running__ = False
        
        self.logging_items = [self.state.name]
        
    def log(self, interval: float):
        previous_time = time.time()
        print(self.logging_items)
        while self.__running__:
            if (time.time() - previous_time)*1000 < interval*1000:
                continue
            previous_time = time.time()
            print(self.logging_items)
        print(self.logging_items)
        
    def use_logs(self, items: list):
        self.logging_items = items
        
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
        player = Rocket(self._window_, Point.fill(64), self.res_scalar)
        dt_last_frame = 0.0
        
        logger = threading.Thread(target=self.log, args=(0.5, ), daemon=True)
        
        just_starting = False
        game_start_time = time.time()
        starting_intermission = 1.0
        
        keys = pygame.key.get_pressed()
        
        self.set_state(GameStates.LAUNCHING)
        logger.start()
        self.mouse.update()
        
        while self.__running__:
            keys = pygame.key.get_pressed()
            self.use_logs([self.state.name])
            
            match self.state:
                case GameStates.LAUNCHING: #reset all values for game start
                    self.set_state(GameStates.MENU)
                case GameStates.MENU:
                    if self.play_button.Lpressed(self.mouse):
                        self.set_state(GameStates.STARTING)
                    elif self.settings_button.Lpressed(self.mouse):
                        self.set_state(GameStates.SETTINGS)
                    elif self.quit_button.Lpressed(self.mouse):
                        self.set_state(GameStates.QUITTING)
                case GameStates.SETTINGS: #settings logic
                    if self.back_button.Lpressed(self.mouse):
                        self.set_state(GameStates.MENU)
                    elif self.fullscreen_button.Lpressed(self.mouse):
                        self.config_settings["fullscreen"] = not self.config_settings["fullscreen"]
                case GameStates.STARTING: #reset all values for game start
                    if not just_starting:
                        just_starting = True
                        game_start_time = time.time()
                    player.at(Point(self._window_.get_width()/2 - player.size.x/2, self._window_.get_height() - player.size.y))
                    if time.time() - game_start_time > starting_intermission:
                        self.set_state(GameStates.PLAYING)
                        just_starting = False
                case GameStates.PLAYING: #gameplay logic
                    if keys[pygame.K_w]:
                        player.move_y(-Settings.player_speed(self.res_scalar).y * dt_last_frame)
                    elif keys[pygame.K_s]:
                        player.move_y(Settings.player_speed(self.res_scalar).y * dt_last_frame)
                    if keys[pygame.K_d]:
                        player.move_x(Settings.player_speed(self.res_scalar).x * dt_last_frame)
                    elif keys[pygame.K_a]:
                        player.move_x(-Settings.player_speed(self.res_scalar).x * dt_last_frame)
                case GameStates.LOST: #lost, ready to go back to menu
                    player.at(player.pos.get_point())
                case GameStates.QUITTING: #final actions before closings
                    player.at(Point.fill(0))
            game_time = round(time.time() - game_start_time, ndigits=1)
            self.graphics(self.state, player, game_time)
            self.mouse.update()
            dt_last_frame = self.clock.tick(self.fps) / 1000
            self.quit_request()
        logger.join()
        pygame.quit()
        Settings.save_settings(self.config_settings)
    
Game("game", 60).run()