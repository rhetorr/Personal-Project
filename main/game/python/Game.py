import time
import threading
import pygame
from GameStates import GameStates
from util.MouseUtil import Mouse, ClickType
from entities.Rocket import Rocket
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
        player = Rocket(self._window_, Point.fill(64), self.res_scalar, self.config_settings["fuel_usage"])
        dt_last_frame = 0.0
        player_bounds = Point(self._window_.get_width()-player.size.x, self._window_.get_height()-player.size.y)
        player_vel = Point(0,0)
        lookahead_player = player.pos.get_point()
        player_speed = Settings.player_speed(self.res_scalar)
        
        logger = threading.Thread(target=self.log, args=(0.5, ), daemon=True)
        
        just_starting = False
        game_start_time = time.time()
        game_time = time.time()
        time_paused = 0
        starting_intermission = 1.0
        time_since_esc = time.time()
        within_window_x = False
        within_window_y = False
        
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
                    game_time = round(time.time() - game_start_time, ndigits=1)
                    if not just_starting:
                        just_starting = True
                        game_start_time = time.time()
                        time_paused = 0
                        player.fuel = 100
                        player.at(Point(self._window_.get_width()/2 - player.size.x/2, self._window_.get_height() - player.size.y - 8))
                    if time.time() - game_start_time > starting_intermission:
                        self.set_state(GameStates.PLAYING)
                        just_starting = False
                case GameStates.PLAYING: #gameplay logic
                    if keys[pygame.K_ESCAPE]:
                        if time_since_esc > 0.2:
                            time_since_esc = 0
                            self.set_state(GameStates.PAUSED)
                    elif player.fuel <= 0:
                        player.fuel = 0
                        self.set_state(GameStates.LOST)
                    else:
                        game_time = round(time.time() - game_start_time - time_paused, ndigits=1)
                        if game_time >= self.config_settings["best_time"]:
                            self.config_settings["best_time"] = game_time
                            
                        if keys[pygame.K_w] and within_window_y:
                            player_vel.y = -player_speed.y * dt_last_frame
                        elif keys[pygame.K_s] and within_window_y:
                            player_vel.y = player_speed.y * dt_last_frame
                        else:
                            player_vel.y = 0
                        if keys[pygame.K_d] and within_window_x:
                            player_vel.x = player_speed.x * dt_last_frame
                        elif keys[pygame.K_a] and within_window_x:
                            player_vel.x = -player_speed.x * dt_last_frame
                        else:
                            player_vel.x = 0
                            
                        lookahead_player = player.pos.get_point().plus(player_vel)
                        within_window_x = 0 < lookahead_player.x and lookahead_player.x < player_bounds.x
                        within_window_y = 0 < lookahead_player.y and lookahead_player.y < player_bounds.y
                        if within_window_x:
                            player.move_x(player_vel.x)
                        if within_window_y:
                            player.move_y(player_vel.y)
                            
                        temp = (0.25) if (player_vel.norm() == 0) else (player_vel.norm()/(player_speed.x*dt_last_frame))
                        player.fuel -= player.fuel_usage * temp
                    time_since_esc += dt_last_frame
                case GameStates.PAUSED:
                    time_paused += dt_last_frame
                    if keys[pygame.K_ESCAPE]:
                        if time_since_esc > 0.2:
                            time_since_esc = 0
                            self.set_state(GameStates.PLAYING)
                    elif self.menu_button.Lpressed(self.mouse):
                        self.set_state(GameStates.MENU)
                    time_since_esc += dt_last_frame
                case GameStates.LOST: #lost, ready to go back to menu
                    player.at(player.pos.get_point())
                    if self.menu_button.Lpressed(self.mouse):
                        self.set_state(GameStates.MENU)
                case GameStates.QUITTING: #final actions before closings
                    player.at(Point.fill(0))
            self.graphics(self.state, player, game_time)
            self.mouse.update()
            dt_last_frame = self.clock.tick(self.fps) / 1000
            self.quit_request()
        logger.join()
        pygame.quit()
        Settings.save_settings(self.config_settings)
    
Game("game", 60).run()