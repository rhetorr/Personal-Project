import random
import time
import threading
import pygame
from GameStates import GameStates
from entities.FuelCell import FuelCell
from entities.Asteroid import Asteroid
from util.MouseUtil import Mouse, ClickType
from entities.Rocket import Rocket
from util.mathextra.Location import Angle, Point, Vector
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
        super().__init__((1200,1000), caption, "icon.png", Mouse())
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
        player_speed = Point(self.bg_vel, self.bg_vel)
        
        fuel_collected = 0
        score = 0
        
        asteroid_1 = Asteroid(self._window_, Point.fill(100), self.res_scalar)
        time_since_asteroid_spawn_1 = 0
        next_asteroid_spawn_1 = 0
        
        asteroid_2 = Asteroid(self._window_, Point.fill(50), self.res_scalar)
        time_since_asteroid_spawn_2 = 0
        next_asteroid_spawn_2 = 0
        
        asteroid_3 = Asteroid(self._window_, Point.fill(25), self.res_scalar)
        time_since_asteroid_spawn_3 = 0
        next_asteroid_spawn_3 = 0
        
        asteroid_4 = Asteroid(self._window_, Point.fill(25), self.res_scalar)
        time_since_asteroid_spawn_4 = 0
        next_asteroid_spawn_4 = 0
        
        asteroid_5 = Asteroid(self._window_, Point.fill(125), self.res_scalar)
        time_since_asteroid_spawn_5 = 0
        next_asteroid_spawn_5 = 0
        
        collided_with_asteroid = False
        
        time_since_fuel_spawn = 0
        next_fuel_spawn = 0
        next_fuel_speed = 0 #px/s
        fuel_cell = FuelCell(self._window_, Point.fill(25).times(self.res_scalar), self.res_scalar)
        
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
                        fuel_collected = 0
                        player.fuel = 100
                        collided_with_asteroid = False
                        asteroid_1.reset()
                        asteroid_2.reset()
                        asteroid_3.reset()
                        asteroid_4.reset()
                        asteroid_5.reset()
                        fuel_cell.reset()
                        self.space_bg_1.at(Point.fill(0))
                        self.space_bg_2.at(Point(0,-self.space_bg_2.size.y+100))
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
                    elif collided_with_asteroid:
                        self.set_state(GameStates.LOST)
                    else:
                        game_time = round(time.time() - game_start_time - time_paused, ndigits=1)
                        if game_time >= self.config_settings["best_time"]:
                            self.config_settings["best_time"] = game_time
                        
                        if self.space_bg_1.pos.y + self.bg_vel*dt_last_frame + 100 > self._window_.get_height():
                            self.space_bg_1.show().at(Point.fill(0)).render()
                            self.space_bg_2.show().at(Point(0,-self.space_bg_2.size.y+100)).render()
                        else:
                            self.space_bg_1.show().move_y(self.bg_vel*dt_last_frame).render()
                            self.space_bg_2.show().move_y(self.bg_vel*dt_last_frame).render()
                            
                        if fuel_cell.spawned:
                            if fuel_cell.collided(player.rect):
                                player.fuel = min(player.fuel + fuel_cell.fuel, self.config_settings["max_fuel"])
                                fuel_collected += 1
                                fuel_cell.reset()
                            elif fuel_cell.pos.y > self._window_.get_height():
                                fuel_cell.reset()
                            else:
                                fuel_cell.move_y(next_fuel_speed * dt_last_frame)
                        else:
                            if time_since_fuel_spawn > next_fuel_spawn:
                                fuel_cell.spawn(random.randint(0, self._window_.get_width()-round(fuel_cell.size.x)))
                                time_since_fuel_spawn = 0
                                next_fuel_spawn = random.randint(3, 10)
                                next_fuel_speed = random.randint(self.bg_vel,self.bg_vel+150)
                            else:
                                time_since_fuel_spawn += dt_last_frame
                        
                        if asteroid_1.spawned:
                            if asteroid_1.collided(player.rect):
                                collided_with_asteroid = True
                            elif asteroid_1.pos.y > self._window_.get_height():
                                asteroid_1.reset()
                            else:
                                asteroid_1.spin()
                                asteroid_1.move_along_path(dt_last_frame)
                        else:
                            if time_since_asteroid_spawn_1 > next_asteroid_spawn_1:
                                asteroid_1.spawn(random.randint(0, self._window_.get_width()-round(asteroid_1.size.x)))
                                time_since_asteroid_spawn_1 = 0
                                next_asteroid_spawn_1 = random.randint(0, 2)
                                asteroid_1.vector = Vector(float(random.randint(self.bg_vel-150, self.bg_vel+100)), Angle.in_degrees(float(random.randint(60, 120))))
                            else:
                                time_since_asteroid_spawn_1 += dt_last_frame
                                
                        if asteroid_2.spawned:
                            if asteroid_2.collided(player.rect):
                                collided_with_asteroid = True
                            elif asteroid_2.pos.y > self._window_.get_height():
                                asteroid_2.reset()
                            else:
                                asteroid_2.spin()
                                asteroid_2.move_along_path(dt_last_frame)
                        else:
                            if time_since_asteroid_spawn_2 > next_asteroid_spawn_2:
                                asteroid_2.spawn(random.randint(0, self._window_.get_width()-round(asteroid_2.size.x)))
                                time_since_asteroid_spawn_2 = 0
                                next_asteroid_spawn_2 = random.randint(1, 4)
                                asteroid_2.vector = Vector(float(random.randint(self.bg_vel-150, self.bg_vel+100)), Angle.in_degrees(float(random.randint(60, 120))))
                            else:
                                time_since_asteroid_spawn_2 += dt_last_frame
                                
                        if asteroid_3.spawned:
                            if asteroid_3.collided(player.rect):
                                collided_with_asteroid = True
                            elif asteroid_3.pos.y > self._window_.get_height():
                                asteroid_3.reset()
                            else:
                                asteroid_3.spin()
                                asteroid_3.move_along_path(dt_last_frame)
                        else:
                            if time_since_asteroid_spawn_3 > next_asteroid_spawn_3:
                                asteroid_3.spawn(random.randint(0, self._window_.get_width()-round(asteroid_3.size.x)))
                                time_since_asteroid_spawn_3 = 0
                                next_asteroid_spawn_3 = random.randint(0, 1)
                                asteroid_3.vector = Vector(float(random.randint(self.bg_vel-150, self.bg_vel+100)), Angle.in_degrees(float(random.randint(60, 120))))
                            else:
                                time_since_asteroid_spawn_3 += dt_last_frame
                                
                        if asteroid_4.spawned:
                            if asteroid_4.collided(player.rect):
                                collided_with_asteroid = True
                            elif asteroid_4.pos.y > self._window_.get_height():
                                asteroid_4.reset()
                            else:
                                asteroid_4.spin()
                                asteroid_4.move_along_path(dt_last_frame)
                        else:
                            if time_since_asteroid_spawn_4 > next_asteroid_spawn_4:
                                asteroid_4.spawn(random.randint(0, self._window_.get_width()-round(asteroid_4.size.x)))
                                time_since_asteroid_spawn_4 = 0
                                next_asteroid_spawn_4 = random.randint(0, 1)
                                asteroid_4.vector = Vector(float(random.randint(self.bg_vel-150, self.bg_vel+100)), Angle.in_degrees(float(random.randint(60, 120))))
                            else:
                                time_since_asteroid_spawn_4 += dt_last_frame
                                
                        if asteroid_5.spawned:
                            if asteroid_5.collided(player.rect):
                                collided_with_asteroid = True
                            elif asteroid_5.pos.y > self._window_.get_height():
                                asteroid_5.reset()
                            else:
                                asteroid_5.spin()
                                asteroid_5.move_along_path(dt_last_frame)
                        else:
                            if time_since_asteroid_spawn_5 > next_asteroid_spawn_5:
                                asteroid_5.spawn(random.randint(0, self._window_.get_width()-round(asteroid_5.size.x)))
                                time_since_asteroid_spawn_5 = 0
                                next_asteroid_spawn_5 = random.randint(2, 4)
                                asteroid_5.vector = Vector(float(random.randint(self.bg_vel-150, self.bg_vel+100)), Angle.in_degrees(float(random.randint(60, 120))))
                            else:
                                time_since_asteroid_spawn_5 += dt_last_frame
                            
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
                    score = round(game_time * max(fuel_collected, 1))
                    self.config_settings["best_score"] = max(self.config_settings["best_score"], score)
                    time_paused += dt_last_frame
                    if keys[pygame.K_ESCAPE]:
                        if time_since_esc > 0.2:
                            time_since_esc = 0
                            self.set_state(GameStates.PLAYING)
                    elif self.menu_button.Lpressed(self.mouse):
                        self.set_state(GameStates.MENU)
                    time_since_esc += dt_last_frame
                case GameStates.LOST: #lost, ready to go back to menu
                    score = round(game_time * max(fuel_collected, 1))
                    self.config_settings["best_score"] = max(self.config_settings["best_score"], score)
                    player.at(player.pos.get_point())
                    if self.menu_button.Lpressed(self.mouse):
                        fuel_cell.reset()
                        self.set_state(GameStates.MENU)
                case GameStates.QUITTING: #final actions before closings
                    player.at(Point.fill(0))
            self.graphics(self.state, player, fuel_cell, asteroid_1, asteroid_2, asteroid_3, asteroid_4, asteroid_5, game_time, score)
            self.mouse.update()
            dt_last_frame = self.clock.tick(self.fps) / 1000
            self.quit_request()
        logger.join()
        pygame.quit()
        Settings.save_settings(self.config_settings)
    
Game("Space Explorer", 60).run()